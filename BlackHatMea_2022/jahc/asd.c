#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

void print_chunk(uint64_t* c){
    puts("-------------------");
    printf("@| %p\n", c);
    printf("0| %p\n", c[-2]);
    printf("1| %p\n", c[-1]);
    printf("2| %p\n", c[0]);
    printf("3| %p\n", c[1]);
    printf("4| %p\n", c[2]);
    printf("5| %p\n", c[3]);
    puts("-------------------");
}
// Get the AMOUNT to shift over for size and the offset on the largebin.
// Needs to be a valid minimum sized chunk in order to work.
int get_shift_amount(char* pointer){

    int shift_amount = 0;
    long long ptr = (long long)pointer;

    while(ptr > 0x20){
        ptr = ptr >> 8;
        shift_amount += 1;
    }

    return shift_amount - 1; // Want amount PRIOR to this being zeroed out
}

int main(){
    uint64_t* a = malloc(0x2000);
    puts("A");
    print_chunk(a);
    uint64_t* b = malloc(0x600); // prevent merge

    uint64_t* c = malloc(0x600);
    int shift = get_shift_amount((char*)a);
    size_t alloc_size = ((size_t)a) >> (8*shift);
    printf("Alloc size 0x%lx\n", alloc_size);

    if(alloc_size < 0x10){
        puts("Too small...");
        exit(1);
    }

    alloc_size = (alloc_size & 0xFFFFFFFFE) - 0x10; // Remove the size bits
    uint64_t* d = malloc(0x600);
    return 0;

}
