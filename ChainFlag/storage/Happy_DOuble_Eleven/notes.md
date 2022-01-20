# SOLUTION

Step 1)

gift()
{balance = [0x64, 1, 1], vals = [0, 0, 0]}

guess()
{balance = [0x64, 1, 1], vals = [0, 1, ?], owncond}


func_06CE(val2 = 1, val3 = ?)
{balance = [0x64, 1, 1], vals = [0, 1, ?], owncond}

buy()
{balance = [0x64, 2, 2], vals = [0, 1, ?], owncond}

retract()
{balance = [0x64, 2, 2], vals = [-1, 1, ?], owncond}

revise()
{balance = [0x64, 2, 3], vals = [-1, 1, ?], owncond, owner}

withdraw()
{balance = [0x64, 2, 3], vals = [-1, 1, ?], owncond, owner}



# payforFlag

Constraints:
- sender == owner
- balance3[sender] == 0x3
- balance2[sender] > 10 Ether

Effect:
- balance[sender] = 0
- apples[sender] = 0
- Val2 &= 0xffffffff..fffffff00

# deposit

Constraints:
- msg.value >= 500 Ether

Effect:
- balance2[sender] += 1

# gift

Constraints:
- sender != contract
- balance2[sender] == 0

Effect:
- balance[sender] = 0x64
- balance2[sender] += 1
- balance3[sender] += 1

# revise

Constraint:
- Val1 > 0xfffffffff...fff00000
- balance2[sender] == 0x2
- balance3[sender] == 0x2
- condition on owner

Effect:
- mapping1[arg0] = arg1 // storage[k(1 + arg0)] = arg1

if Val1 >= 0xffffffff0000...
- balance3[sender] += 1
else:
- storeIncrement(0x1,0x0) // Val1 = 0


# func_06CE

Effect:
- Can control Val3 and Val2 via result to contract call


# guess

Constraint:
- little guess on block hash

Effect:
- unset inital owner bits

# buy

Constraints:
- balance2 == 1
- balance3 == 1
- val2 == 1
- condition on owner

Effect:
- balance2 += 1
- balance3 += 1

# retract

Contraints
- Val1 == 0
- balance2[sender] == 2
- balance3[sender] == 2
- cond on owner

Effect:
- Val1 -= 1

# withdraw

Constrains:
- sender == owner
- balance2[sender] == 2
- balance3[sender] == 3
- balance1[sender] < arg0

Effect:
- balance1[sender] -= arg0
- call(sender).value(balance1[arg0])
- balance2[sender] -= 1

# transfer

Constraints:
- arg1 != 0
- arg2 > 0
- balance1[sender] >= arg2
- balance1[arg1] + arg2 > balance[arg1]

Effect:
- balance1[sender] -= arg2
- balance1[arg1] += arg2
