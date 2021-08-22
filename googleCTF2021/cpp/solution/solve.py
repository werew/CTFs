from z3 import *

ROM = [0]*158
ROM[0] = 0b10111011;
ROM[1] = 0b01010101;
ROM[2] = 0b10101011;
ROM[3] = 0b11000101;
ROM[4] = 0b10111001;
ROM[5] = 0b10011101;
ROM[6] = 0b11001001;
ROM[7] = 0b01101001;
ROM[8] = 0b10111011;
ROM[9] = 0b00110111;
ROM[10] = 0b11011001;
ROM[11] = 0b11001101;
ROM[12] = 0b00100001;
ROM[13] = 0b10110011;
ROM[14] = 0b11001111;
ROM[15] = 0b11001111;
ROM[16] = 0b10011111;
ROM[17] = 0b00001001;
ROM[18] = 0b10110101;
ROM[19] = 0b00111101;
ROM[20] = 0b11101011;
ROM[21] = 0b01111111;
ROM[22] = 0b01010111;
ROM[23] = 0b10100001;
ROM[24] = 0b11101011;
ROM[25] = 0b10000111;
ROM[26] = 0b01100111;
ROM[27] = 0b00100011;
ROM[28] = 0b00010111;
ROM[29] = 0b00100101;
ROM[30] = 0b11010001;
ROM[31] = 0b00011011;
ROM[32] = 0b00001000;
ROM[33] = 0b01100100;
ROM[34] = 0b01100100;
ROM[35] = 0b00110101;
ROM[36] = 0b10010001;
ROM[37] = 0b01100100;
ROM[38] = 0b11100111;
ROM[39] = 0b10100000;
ROM[40] = 0b00000110;
ROM[41] = 0b10101010;
ROM[42] = 0b11011101;
ROM[43] = 0b01110101;
ROM[44] = 0b00010111;
ROM[45] = 0b10011101;
ROM[46] = 0b01101101;
ROM[47] = 0b01011100;
ROM[48] = 0b01011110;
ROM[49] = 0b00011001;
ROM[50] = 0b11111101;
ROM[51] = 0b11101001;
ROM[52] = 0b00001100;
ROM[53] = 0b11111001;
ROM[54] = 0b10110100;
ROM[55] = 0b10000011;
ROM[56] = 0b10000110;
ROM[57] = 0b00100010;
ROM[58] = 0b01000010;
ROM[59] = 0b00011110;
ROM[60] = 0b01010111;
ROM[61] = 0b10100001;
ROM[62] = 0b00101000;
ROM[63] = 0b01100010;
ROM[64] = 0b11111010;
ROM[65] = 0b01111011;
ROM[66] = 0b00011011;
ROM[67] = 0b10111010;
ROM[68] = 0b00011110;
ROM[69] = 0b10110100;
ROM[70] = 0b10110011;
ROM[71] = 0b01011000;
ROM[72] = 0b11000110;
ROM[73] = 0b11110011;
ROM[74] = 0b10001100;
ROM[75] = 0b10010000;
ROM[76] = 0b00111011;
ROM[77] = 0b10111010;
ROM[78] = 0b00011001;
ROM[79] = 0b01101110;
ROM[80] = 0b11001110;
ROM[81] = 0b11011111;
ROM[82] = 0b11110001;
ROM[83] = 0b00100101;
ROM[84] = 0b10001101;
ROM[85] = 0b01000000;
ROM[86] = 0b10000000;
ROM[87] = 0b01110000;
ROM[88] = 0b11100000;
ROM[89] = 0b01001101;
ROM[90] = 0b00011100;

FLAG = [0]*27
for i in range(len(FLAG)):
    FLAG[i] = BitVec("Flag_%d"%i,8)
    #FLAG[i] = 97
    ROM[128+i] = FLAG[i]


A = 0;
B = 0;
Z = 0;
X = 0;
Y = 0;
O = 0;
C = 0;

I = 0;
M = 0;
N = 1;
P = 0;
Q = 0;

while True:

    B = (229 + I) & 0xff;
    if B == 0:
        print("SOLVER ")
        print(f"Q {Q}")
        print(f"I {I}")
        print(f"Z {Z}")
        print(f"A {A & 0xff}")
        s = Solver()
        s.add((Q & 0xff) == 0)
        s.add(FLAG[0]  == ord("C"))
        s.add(FLAG[1]  == ord("T"))
        s.add(FLAG[2]  == ord("F"))
        s.add(FLAG[3]  == ord("{"))
        s.add(FLAG[26] == ord("}"))
        print(s.check())
        print(s.model())
        exit(0);

    else:

        A = ROM[128+I]
        B = ROM[I]
        print(f"S36: A {A & 0xff}")
        print(f"S36: B {B & 0xff}")
        X = 1
        Y = 0

        # Compute Y
        while X != 0:
            print(f"S14: X {X} I {I}")
            print(f"S14: Z {Z}")
            Z = X & B
            Z &= 0xff #
            if Z != 0:
              Y += A
              Y &= 0xff #
            X += X
            X &= 0xff #
            A += A
            A &= 0xff #

        A = Y
        print(f"S23: A {A & 0xff}")
        Z = 1

        print(f"S38: M {M & 0xff}")
        O = M
        O += N
        O &= 0xff #
        M = N
        N = O

        A += M
        A &= 0xff #
        print(f"S43: M {M & 0xff}")
        print(f"S43: A {A & 0xff}")

        B = 32
        B += I
        B &= 0xff
        A ^= ROM[B]
        print(f"S47: A {A & 0xff}")

        P += A
        P &= 0xff #
        print(f"S48: P {P & 0xff}")

        B = 64
        B += I
        B &= 0xff
        A = ROM[B]
        print(f"S51: A {A & 0xff}")

        A ^= P
        Q |= A
        Q &= 0xff
        A = 1

        print(f"S51: A {A & 0xff}")
        print(f"S51: P {Q & 0xff}")

        I += A
