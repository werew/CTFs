import gdb
import sys
import struct

THE_END = False
MY_BP_HANDLERS = {}

def ExprAsInt(expr):
  return int(str(gdb.parse_and_eval("(void*)(%s)" % expr )).split(" ")[0], 16)

def BreakHandler(ev):
  global MY_BP_HANDLERS

  eip = ExprAsInt("$rip")
  #print("~" * 70, hex(eip))
  
  if ev.__class__ != gdb.BreakpointEvent:

    print("Not a breakpoint; not handled")
    print(gdb.execute("info reg", False, True))

    eip = ExprAsInt("$rip")
    print(gdb.execute("where 10", False, True))
    sys.exit(0)

  #print "Break!"
  for bp in ev.breakpoints:
    if eip in MY_BP_HANDLERS:
      MY_BP_HANDLERS[eip](ev.breakpoints, eip)
      gdb.execute("continue", False)
    else:
      print("----> Unknown BP!")
      print(gdb.execute("x/1i $rip", False, True))




def SetBP(addr, handler):
  gdb.execute("break *0x%x" % addr, False)
  MY_BP_HANDLERS[addr] = handler

# Set some GDB stuff.
gdb.execute("set python print-stack full", False, True)    
gdb.execute("set disassembly-flavor intel", False)
gdb.execute("set height 0", False)
gdb.events.stop.connect(BreakHandler)

style = "bx"

def encrypt_2_in(ev,eip):
  print("Encrypt_2 IN")
  gdb.execute("x/16"+style+" *(long int*)($rbp-0x50)", False)

def encrypt_2_out(ev,eip):
  print("Encrypt_2 OUT")
  gdb.execute("x/16"+style+" *(long int*)($rbp-0x50)", False)

def encrypt_2_in_2(ev,eip):
  print("Encrypt_2 IN 2")
  gdb.execute("x/16"+style+" *(long int*)($rbp-0x50)", False)

def encrypt_2_out_2(ev,eip):
  print("Encrypt_2 OUT 2")
  gdb.execute("x/16"+style+" *(long int*)($rbp-0x50)", False)

def the_end(ev,eip):
  print("THE END")
  gdb.execute("x/16"+style+" *(long int*)($rbp-0x50)", False)




SetBP(0x00463703,encrypt_2_in)
SetBP(0x00463708,encrypt_2_out)
"""
SetBP(0x00463c59,encrypt_2_in_2)
SetBP(0x00463c5e,encrypt_2_out_2)
SetBP(0x00463c81,the_end)
"""




#gdb.execute("run AAAAAAAAAAAAAAAA")
#gdb.execute("run 0123456789ABCDEF")
#gdb.execute("run A123A123A123A123")
gdb.execute("run A1AAA2AAA3AAA4AA")


