from bitarray import bitarray
from pwn import *


f = "0x1.5577557667557p+63"
f = "0x1.0aecce8effd08p+50"
sign = '0' if f.startswith('-') else '1'

fr, exp = f.split('.')[1].split('p')

def rev(a):
    return ''.join(reversed(a))

def pad(a, n):
    if len(a) < n:
        return (n-len(a))*'0'+a
    return a

exp = (pad(bin(int(exp) + 960)[2:],11))
fr = (pad(bin(int(fr,16))[2:],52))

res = f'0b{sign}{fr}{exp}'
print(res)
print(hex(int(res,2)))
