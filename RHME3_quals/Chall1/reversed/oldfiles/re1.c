

int main(...){

    setup1();
}


encrypt_1(char* arg_copy, char *buff){
    
    int i10, i18, i20, i28;
    trampoline8 = 0x14; //20

trampoline:

    switch(trampoline8){

// Copy into buf
        case 0x14:
                i28 = 0;
                trampoline8 = 0x12; 
            break;
        case 0x12:
                if (i28 > 0xf){
                    trampoline8 = 0xf;
                } else {
                    trampoline8 = 0x10;
                }
            break;
        case 0x10:
                buff[i28] = arg_copy[i28];
                i28 += 1;
                trampoline8 = 0x12
                
            break;

//
        case 0xf:
                i20 = 0;
                trampoline8 = 0xd
            break;
        case 0xd:
               if (i20 > 0x8){
                    trampoline8 = 0x5;
                } else {
                    trampoline8 = 0xb;
                } 
            break;
        case 0xb:   // This x9
               encrypt_2(buff);  // Mangle
               i18 = 0;
                trampoline8 = 0x9;
            break;
        case 0x9:
             if (i18 > 0x3){
                trampoline8 = 0x6
            } else {
                trampoline8 = 0x7
            }
            break;
        case 0x7:  //  x9    This x4
            /* ENCRYPTION BLOB */
            /* encrypt 4 chars of buffer starting from i18 */
            i18 += 1;
            trampoline8 = 0x9;
            break;
        case 0x6:
            i20 += 1;
            trampoline8 = 0xd;
            break;

//
        case 0x5:
            encrypt_2(buff); // Mangle
            i10 = 0;
            trampoline8 = 0x3;
            break;
        case 0x3:
            if (i10 > 0xf){
                trampoline8 = 0x0;
            } else {
                trampoline8 = 0x1;
            }
            break;
        case 0x1:
            /* BLOB (small)*/
            // How is it generated the table at 
            // 0x6651c0 ... 0x6651c0+0xf00+0xff
            // ???? 
            // aka table2 
            buff[i10] = 0x6651c0[ buff[i10] + (i10 << 8)]
            trampoline8 = 0x3;
            i10 += 1;
            break;
        case 0x0:
            return;
            break;
    }
    goto trampoline;
    


}

/*
4141 4141 4141 4141 4141 4141 4141 4141
???????????????????????????????????????   // encrypt_2  ---> 0xb
5d8d b4af e143 bf17 2e1f fe36 38d8 3fa6   // BLOB       ---> 0x7
5d43 fea6 e11f 3faf 2ed8 b417 388d bf36   // encrypt_2
30d3 ecd4 c5bb a694 7d92 2846 fde6 df21   // BLOB
30bb 2821 c592 dfd4 7de6 ec94 fdd3 a646   // encrypt_2
dd8c 46d2 c930 d7d6 1100 88f1 4a74 847a   // BLOB
dd30 887a c900 84d2 1174 46d6 4a8c d7f1   // encrypt_2
b409 0424 8a64 9e1d 924d ea01 e872 b399   // BLOB
b464 ea99 8a4d b324 9272 041d e809 9e01   // encrypt_2
e6f7 b3f2 84cc 2eef 0dd1 a9fa 836c e592   // BLOB
e6cc a992 84d1 e5f2 0d6c b3ef 83f7 2efa   // encrypt_2
194c 7d19 32b7 4c21 2347 13a7 219b eeb7   // BLOB
19b7 13b7 3247 ee19 239b 7d21 214c 4ca7   // encrypt_2
c69f 5685 a01b e123 7c06 0852 e1db 7970   // BLOB
c61b 0870 a006 7985 7cdb 5623 e19f e152   // encrypt_2
1c90 be91 4bbe 3283 612f 09b5 8eea 510b   // BLOB
1cbe 090b 4b2f 5191 61ea be83 8e90 32b5   // encrypt_2
c081 dec4 7fae f94d 1fc5 b610 086e aca9   // BLOB
c0ae b6a9 7fc5 acc4 1f6e de4d 0881 f910   // encrypt_2 ---> 0x5

35ae b6a9 7fc5 acc4 1f6e de4d 0881 f910   // BLOB      ---> 0x1
3576 b6a9 7fc5 acc4 1f6e de4d 0881 f910   // BLOB
3576 d5a9 7fc5 acc4 1f6e de4d 0881 f910   // BLOB
......
3576 d57f e52c 7aee 387e de9a c097 7e2e   // BLOB: Done!
*/




i10= 0...0xf
blob2 {
    buff[i10] = 0x6651c0[ buff[i10] + (i10 << 8)]
}
