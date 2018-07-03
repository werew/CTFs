#include <string.h>
#include <stdio.h>
#include <unistd.h>



int main(int argc, char* argv[]){

    char buf[1024];

    FILE* f = fopen(argv[1],"r");
    if (f == NULL) {
        puts("cannot open file"); 
        return 1;
    }

    while (1) {
        size_t len = fread(buf, 1, 1024, f);
        if (len == 0) break;

        int i,j;
        for (i=0; i < len; i++){    

            // Convert each 1 bit to 0x0 and each 0 bit to 0xff
            for (j = 0; j < 8; j++){
               char bit = buf[i] & (0x80 >> j); 

               if (bit != 0)
                   write(1,"\x0",1);
                else
                   write(1,"\xff",1);
            }
        }
    }
    return 0;
}

