l = [3,3,4,2,1,2,3,4,1,4,3,2,1,3,2,4,1]
t = "theresanotherstep"

s = ''
for m,c in zip(l,t):
    s += chr(ord(c)+m)

print s
