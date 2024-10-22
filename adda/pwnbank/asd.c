#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(){
    //uint64_t d = (0xaabbaabb33aabbff);
    //uint64_t d = (0x42bb33a3bff42);
    uint64_t d = (0x8000000000000000);
    printf("%a\n",(double)(d));
    double a;
    scanf("%la", &a);
    printf("%lx\n",(long )(a));

    return 0;
}
