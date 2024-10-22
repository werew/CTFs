#!/usr/bin/env python3

from pwn import *

# ----------- Configuration ------------

# Configure accordingly
BINARY = './main'
HOST, PORT = 'localhost', 1337
LIBC = None # Example: './libc-2.27.so'
LD   = None # Example: './ld.so.2' 

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
    return process(args, **kwargs, stdout=process.PTY, stdin=process.PTY)

def start():
    if args.REMOTE:
        log.info("REMOTE PROCESS")
        HOST, PORT = 'blackhat4-26cefe1e3f69295ff4899537770f670e-0.chals.bh.ctf.sa', 443                                                                                                      
        return remote(HOST, PORT, ssl=True, sni=HOST)
        return remote(HOST, PORT)

    elif args.DBG or args.DEBUG:
        log.info("LOCAL PROCESS (DEBUG)")
        return run_debug(BINARY, libc=LIBC, ld=LD)

    else:
        log.info("LOCAL PROCESS")
        return run_plain(BINARY, libc=LIBC, ld=LD)

# ----------- Functions -------------

def add(content):
    p.sendlineafter('> ', '1')
    p.sendlineafter('> ', content)

def show():
    p.sendlineafter('> ', '2')

def free():
    p.sendlineafter('> ', '3')


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

# Profit
p.interactive()

