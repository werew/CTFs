int main(){

    if (write(1,0x14,"inizia...") != 0x14) exit(0);

    sleep(5);
    alarm(0x1e); //set an alarm clock for delivery of a signal

    if (write(1,0x6,"ready") != 0x6) exit(0);

    while (1) { do_test(0); }
}

#define PROT_READ   0x1     /* Page can be read.  */
#define PROT_WRITE  0x2     /* Page can be written.  */
#define PROT_EXEC   0x4     /* Page can be executed.  */
#define PROT_NONE   0x0     /* Page can not be accessed.  */
#define MAP_PRIVATE 0x02
#define MAP_ANONYMOUS 0x20 

alloc_page(){
   return mmap(0,0x1000,3,0x22,-1,NULL);
}


(rdi,rsi,rdx)
read_inst(rdi,rsi,rdx)

do_test(){

    /********** SETUP ***************/
    rbx = alloc_page();

    // copy template stuct
    p[0] = obj.template[0]
    p[8] = obj.template[8]
    p[0xc] = obj.template[0xc]
    p[0xe] = obj.template[0xe]

    read_inst(&p[5]);// 4 bytes inst
    make_page_executable(p);
    // -> mprotect(....)



    /*********** START *************/
    r12 = read_time_stamp_counter();

    rbx();

    r12 = read_time_stamp_counter();
}



