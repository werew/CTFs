0x6000 :  call 0x60006                          (0600000006060000)
0x6005 :  powerdown 0000
0x6006 :  mov_data 31054040000006060000 (reg 5:  ( 0x60040 + 0x60040i ))
0x600b :  mov_data 31030400000000000000 (reg 3:  ( 0x4 + 0x0i ))
0x6010 :  mov_data 31060100000000000000 (reg 6:  ( 0x1 + 0x0i ))
0x6015 :  syscall 4903 (syscall 3) print edi (print "EasyPwn")

0x6016 :  mov_data 31054041000006060000
0x601b :  mov_data 31030900000000000000
0x6020 :  syscall 4903             print "How many strings:" 

0x6021 :  mov_data 31044045000006060000 esi
0x6026 :  mov_data 31010001000000000000
0x602b :  syscall 4905  ecx = readint(64)

0x602c :  mov_data 31054042000006060000
0x6031 :  mov_data 31030900000000000000
0x6036 :  syscall 4903 print edi (print "Input:")

0x6037 :  mov_reg 4145   reg5 <- reg4 ; edi = esi
0x6038 :  mov_data 31031000000000000000  edx = 0x10
0x603d :  syscall 4902 writeMem(at: edi=0x60040, size: edx=0x10, read(64))

0x603e :  add 3014 reg4 += reg1 (esi += ebx)
0x603f :  jmpne 47002c00000006060000 ecx--, if ecx != 0 jmp
0x6044 :  mov_data 31054043000006060000
0x6049 :  mov_data 31030900000000000000
0x604e :  syscall 4903  print "How many letters:"

0x604f :  syscall 4905 ecx = readint(64)

0x6050 :  mov_data 31054044000006060000
0x6055 :  mov_data 31031000000000000000
0x605a :  syscall 4903 print "Your name please:"

0x605b :  sub 48071000000000000000
0x6060 :  mov_reg 4175
0x6061 :  mov_reg 4123
0x6062 :  syscall 4902

0x6063 :  syscall 4903

0x6064 :  sub 4807f000ff00ff00ff00
0x6069 :  ret 4600
