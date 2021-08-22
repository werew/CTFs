#include <stdio.h>
#include <stdlib.h>

unsigned char ROM[155];


int chall(unsigned char flag[26]){

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
    int i;
    for (i=0; i<sizeof(*flag);i++){
      ROM[128+i] = flag[i];
    }


    unsigned int  A = 0;
    unsigned int  B = 0;
    unsigned int  Z = 0;
    unsigned int  X = 0;
    unsigned int  Y = 0;
    unsigned int  O = 0;
    unsigned int  C = 0;

    // b0_28
    unsigned int  I = 0;
    unsigned int  M = 0;
    unsigned int  N = 1;
    unsigned int  P = 0;
    unsigned int  Q = 0;

    while (1) {

      // b29_31
      B = 229 + I;
      B &= 0xff;
      if (B == 0){

        // b56
        if (Q == 0){
          // WIN
          puts("WON");
          abort();
        } else {
          // INVALID FLAG
          //puts("INVALID FLAG");
          return I;
        }

      } else {

        // b32_14
        A = ROM[128+I]; // FLAG[I]
        B = ROM[I]; // ROM[I]
        X = 1;
        Y = 0;

        // Compute Y = ..
        while (X != 0) {
            // b15_17
            Z = X | B;
            Z &= 0xff;
            if (Z != 0){
              // b18
              Y += A;
              Y &= 0xff;
            } 
            // b19_21
            X += X;
            X &= 0xff;
            A += A;
            A &= 0xff;
        }

        // b22_5
        A = Y;
        printf("A %d\n",A);
        Z = 1;

        // b38_55
        O = M;
        O += N;
        O &= 0xff;
        M = N;
        N = O;

        A += M;
        A &= 0xff;
        A ^= ROM[I];
        P += A;
        P &= 0xff;
        A = ROM[64+I];
        A ^= P;
        Q |= A;

        I += 1;
    }
  }
}

int main(){


  unsigned char FLAG[26];
  int i;
  for (i=0;i<sizeof(FLAG);i++){
    unsigned char c;

    for (c=0; c<=0xff;c++){
      FLAG[i] = c;
      int c_i = chall(FLAG);
      if (c_i >= i){
        printf("%d %d %c\n",i,c_i,c);
        break;
      }
    }
  }
  return 0;
}
