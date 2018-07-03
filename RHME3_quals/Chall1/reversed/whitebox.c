// function @  0x00463631
encrypt(uint8_t* in, uint8_t *out){
 
    int i,j;
    uint8_t *state = out;
 
    // Copy user input
    while (i=0; i < 16; i++){
        state[i] = in[i];  
    }
 
    // First 9 rounds
    for (i=0; i < 9; i++){
        shiftRows(state);       // 0x004634fe
        for (j=0; j<4; j++){  
            blob(i,j,state);    // 0x0046373e
        }    
    }
 
    // The last round I suppose
    shiftRows(state);           // 0x004634fe
 
    // SubBytes + AddRoundKey ???
    for (i=0; i<16; i++){
        state[i] = 0x6651c0[ state[i] + (i << 8)];  // 0x00463c8b
    }
}
 
 
// Blob @ 0x0046373e
// i => round
// j => column
// SubBytes + MixColumn + AddRoundkey ???
blob(i, j, state){
    uint32_t buff[4]; //NB each element is a dword
    buff[0] = 0x6661c0[(state[i*4] + (j*16 + i*4)*256) * 4];
    buff[1] = 0x6661c0[(state[i*4 + 1] + (j*16 + i*4 + 1)*256) * 4];
    buff[2] = 0x6661c0[(state[i*4 + 2] + (j*16 + i*4 + 2)*256) * 4];
    buff[3] = 0x6661c0[(state[i*4 + 3] + (j*16 + i*4 + 3)*256) * 4];
 
    // Compute 1st element of the column
    // Note that the lookup table at 0x6650c0 is just performing xor operations
    // ex: 0x6650c0[0x5d] = 0x5 ^ 0xd
 
    a = 0x6650c0[(buff[0] & 0xf)*16 + (buff[1] & 0xf)];
    b = 0x6650c0[(buff[2] & 0xf)*16 + (buff[3] & 0xf)];
    c = 0x6650c0[((buff[0]/16) & 0xf)*16 + (buff[1]/16) & 0xf];
    d = 0x6650c0[((buff[2]/16) & 0xf)*16 + (buff[3]/16) & 0xf];
    state[i*4] = 0x 6650c0[(c*16) + d]*16 | 0x6650c0[(a*16) + b];
 
    /* A similar pattern is repeated for the 3 remaining elements of the column */
 
    ...
}
