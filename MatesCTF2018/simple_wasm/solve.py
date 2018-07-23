import sys

def dist(a, b):
    if (a < b):
        return b - a
    else:
        return a - b


isvalid = lambda x,y: dist(x,y) > 1

def list2int(l):
    if not l: return 0
    return int(''.join(map(str,l)))

def int2list(n):
    return [int(i) for i in str(n)]

def make_nines(n):
    return [9 for _ in range(n)]


def get_invalids(l):

    if len(l) < 2: return 0   # One digit is always invalid

    total = 0

    for i in range(1,l[0]):   # The last is a special case
        total += get_sub_all(i,len(l)-1)

    tmp = get_sub(l[0],l[1:])
    total += tmp

   
    nines = make_nines(len(l)-1)
    return total + get_invalids(nines)

def get_valids(n):
    return n-get_invalids(int2list(n)) 

lt = {} # We store here the precomputed values
def get_sub_all(i,size):
    if (i,size) in lt:
        return lt[(i,size)]
    else:
        tmp = get_sub(i,make_nines(size))
        lt[(i,size)] = tmp
        return tmp

# Fixed i
def get_sub(i,l):

    if len(l) == 0: return 0

    total = 0

    for j in range(l[0]):
        if isvalid(i,j):
            total += get_sub_all(j,len(l)-1)
        else:
            total += int(pow(10,len(l)-1))

    if isvalid(i,l[0]):
        total += get_sub(l[0],l[1:])
    else:
        total += list2int(l[1:])+1

    return total   



n = int(sys.argv[1])
#print get_valids(int("9"*32))
#quit()

def bin_search(n):
    x = 0                               
    y = 9999999999999999999999999999999999999999999999999999999
    
    while abs(x-y) > 1:
        m = x + (y-x)//2
        if get_valids(m) < n: #14827558276137:
            x = m
        else:
            y = m
    
        print x,y

    if get_valids(x) == n:
        print "------>",x
        return x
    else:
        print "------>",y
        return y

number = bin_search(n)
print number
