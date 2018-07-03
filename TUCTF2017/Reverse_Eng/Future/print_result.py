Flag = [0] * 25

Flag[22]= 110
Flag[16]= 95
Flag[24]= 125
Flag[5]= 123
Flag[4]= 70
Flag[3]= 84
Flag[2]= 67
Flag[1]= 85
Flag[0]= 84
Flag[21]= 119
Flag[17]= 52
Flag[18]= 95
Flag[19]= 100
Flag[15]= 102
Flag[23]= 33
Flag[14]= 48
Flag[20]= 48
Flag[13]= 95
Flag[10]= 51
Flag[8]= 53
Flag[12]= 53
Flag[6]= 53
Flag[11]= 109
Flag[7]= 121
Flag[9]= 55


out = ""
for c in Flag:
    out += chr(c)

print out
