constant_1 = 0x67d25391
constant_2 = 0x328f3b

# eax = constant_1_constant_2 % 10
modulo = 0x00328f3b67d25391 % 10
eax = 0x00328f3b67d25391 / 10

input[counter] = input[counter] - modulo
