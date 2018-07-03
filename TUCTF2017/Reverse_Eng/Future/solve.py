from z3 import *


# Prepare flag
flag = []
for i in range(25):
    flag.append(BitVec("Flag_%d"%i,8))

# Create matrix
mat = [[0 for x in range(5)] for y in range(5)] 
    
for i in range(25):
    m = (i * 2) % 25
    f = (i * 7) % 25
    mat[m/5][m%5] = flag[f]

# Create auth
auth = []
auth.append(mat[0][0] + mat[4][4])
auth.append(mat[2][1] + mat[0][2])
auth.append(mat[4][2] + mat[4][1])
auth.append(mat[1][3] + mat[3][1])
auth.append(mat[3][4] + mat[1][2])
auth.append(mat[1][0] + mat[2][3])
auth.append(mat[2][4] + mat[2][0])
auth.append(mat[3][3] + mat[3][2] + mat[0][3])
auth.append(mat[0][4] + mat[4][0] + mat[0][1])
auth.append(mat[3][3] + mat[2][0])
auth.append(mat[4][0] + mat[1][2])
auth.append(mat[0][4] + mat[4][1])
auth.append(mat[0][3] + mat[0][2])
auth.append(mat[3][0] + mat[2][0])
auth.append(mat[1][4] + mat[1][2])
auth.append(mat[4][3] + mat[2][3])
auth.append(mat[2][2] + mat[0][2])
auth.append(mat[1][1] + mat[4][1])

# Add conditions
s = Solver()
s.add(auth[0] == 0x8b)
s.add(auth[1] == 0xce)
s.add(auth[2] == 0xb0)
s.add(auth[3] == 0x89)
s.add(auth[4] == 0x7b)
s.add(auth[5] == 0xb0)
s.add(auth[6] == 0xb0)
s.add(auth[7] == 0xee)
s.add(auth[8] == 0xbf)
s.add(auth[9] == 0x92)
s.add(auth[10] == 0x65)
s.add(auth[11] == 0x9d)
s.add(auth[12] == 0x9a)
s.add(auth[13] == 0x99)
s.add(auth[14] == 0x99)
s.add(auth[15] == 0x94)
s.add(auth[16] == 0xad)
s.add(auth[17] == 0xe4)


# Printable chars
for i in range(25):
    s.add(flag[i] > 0x20, flag[i] < 0x7f)

# Force flag format
s.add(flag[0] == 0x54) # T
s.add(flag[1] == 0x55) # U
s.add(flag[2] == 0x43) # C
s.add(flag[3] == 0x54) # T
s.add(flag[4] == 0x46) # F
s.add(flag[5] == 0x7B) # {
s.add(flag[24] == 0x7D) # }


print s.check()
print s.model()
