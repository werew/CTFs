
encrypt_1(char* arg_copy, char *buff){
    
    int i10, i18, i20, i28;
    trampoline8 = 0x14; //20

    // Copy
    i28 = 0;             // -> 0x14
    while (i28 <= 0xf){  // -> 0x12
        buff[i28] = arg_copy[i28];  // -> 0x10
        i28++;
    }

    //
    i20 = 0;            // -> 0xf
    while (i20 <= 0x8){ // -> 0xd
        mangle(buff);   // -> 0xb
        i18 = 0;
        while (i18 <= 0x3){ // -> 0x9
            // Blob         // -> 0x7
            i18++;
        }
        i10++;          // -> 0x6
    }

    //
    mangle(buff);       // -> 0x5
    i10 = 0;
    while (i10 <= 0xf){ // -> 0x3
        buff[i10] = 0x6651c0[ buff[i10] + (i10 << 8)] // -> 0x1
        i10++;
    } 
}


blob1(i20, i18, buff){

/*
    rax = buff[i18*4]
    rdx = i18*4 + (i20 << 4)
    var38 = table3[rax + rdx<<8] 

    rcx = rdx = (i18<<2) + c;
    eax = buff[ rdx ]
    rdx = (i20<<4 + rcx) << 8
    rax = eax + rdx
    var38 = table3[rax*4]     // dword
*/

    var38 = table3[ // 4 bytes
        (buff[i18*4] + (i20*16 + i18*4)*256) * 4
    ]

    var34 = table3[
        (buff[i18*4 + 1] + (i20*16 + i18*4 + 1)*256) * 4
    ]

    var30 = table3[
        (buff[i18*4 + 2] + (i20*16 + i18*4 + 2)*256) * 4
    ]

    var2c = table3[
        (buff[i18*4 + 3] + (i20*16 + i18*4 + 3)*256) * 4
    ]


//************************

//    rax = buff + i18*4
/*
    i = ((var38 & 0xf)<<4) + (var34 & 0xf) // 0x0046385d 
    ecx = table1[i]
    i = ((var30 & 0xf)<<4) + (var2c & 0xf)
    edx = table1[i]
    r8d = table1[(rcx << 4) + rdx] //0x004638bd

    i = (((var38>>4)&0xf) << 4) + ((var34>>4) & 0xf)
    ecx = table1[i] // 0x004638ec 
    i = (((var30>>4)&0xf) << 4) + ((var2c>>4) & 0xf)
    edx = table1[i] 

    buff[i18*4] = table1[(rcx << 4) + rdx] | r8d
*/

    
    a = table1[(var38 & 0xf)*16 + (var34 & 0xf)]
    b = table1[(var30 & 0xf)*16 + (var2c & 0xf)]
    c = table1[((var38/16) & 0xf)*16 + (var34/16) & 0xf]
    d = table1[((var30/16) & 0xf)*16 + (var2c/16) & 0xf]

    buff[i18*4] = table1[(c*16) + d]*16 | 
                  table1[(a*16) + b]

    

    i = (((var38>>8) & 0xf)<<4 + (var34>>8) & 0xf) // 0x0046385d 
    ecx = table1[i]
    i = (((var30>>8) & 0xf)<<4 + (var2c>>8) & 0xf) // 0x0046385d 
    edx = table1[i]
    r8d = table1[(rcx << 4) + rdx] //0x004638bd

    i = (((var38>>0xc)&0xf) << 4) + ((var34>>0xc) & 0xf)
    ecx = table1[i] // 0x004638ec 
    i = (((var30>>0xc)&0xf) << 4) + ((var2c>>0xc) & 0xf)
    edx = table1[i] 

    buff[i18*4 + 1] = table1[(rcx << 4) + rdx]<<4 | r8d

}
                


