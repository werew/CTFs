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
  print("------>", MY_BP_HANDLERS[eip])
  print("~" * 70, hex(eip))
  gdb.execute("continue", False)
"""  
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
"""




def SetBP(addr):
  gdb.execute("break *0x%x" % addr, False)

# Set some GDB stuff.
gdb.execute("set python print-stack full", False, True)    
gdb.execute("set disassembly-flavor intel", False)
gdb.execute("set height 0", False)
gdb.events.stop.connect(BreakHandler)



SetBP(0x00463631) 
MY_BP_HANDLERS[0x00463631] = "encrypt1"
SetBP(0x004634fe) 
MY_BP_HANDLERS[0x004634fe] = "mangle"
SetBP(0x0046373e) 
MY_BP_HANDLERS[0x0046373e] = "blob1"
SetBP(0x00463c8b) 
MY_BP_HANDLERS[0x00463c8b] = "blob2"


gdb.execute("run AAAAAAAAAAAAAAAA")


