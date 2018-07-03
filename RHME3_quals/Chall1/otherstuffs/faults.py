import gdb
import sys
import struct
import random
import string

THE_END = False
MY_BP_HANDLERS = {}

def ExprAsInt(expr):
  return int(str(gdb.parse_and_eval("(void*)(%s)" % expr )).split(" ")[0], 16)


def BreakHandler(ev):
  global MY_BP_HANDLERS
  eip = ExprAsInt("$rip")
  print("Break!!!!!!!!!!!") 
  if ev.__class__ != gdb.BreakpointEvent:

    print("Not a breakpoint; not handled")
    print(gdb.execute("info reg", False, True))

    eip = ExprAsInt("$rip")
    print(gdb.execute("where 10", False, True))
    sys.exit(0)

  for bp in ev.breakpoints:
    if eip in MY_BP_HANDLERS:
      MY_BP_HANDLERS[eip](ev.breakpoints, eip)
      gdb.execute("continue",False)
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



############# Actual script #################

random.seed(0) # So we get predictable values, useful for debugging


def randInput():
  return ''.join(random.choice(string.ascii_letters + string.digits) 
            for _ in range(16))

def printBytes(b):
  print('~ '+(''.join("%02x" % i for i in b)))

def readBytes(nb, addr):
  print("reading")
  b = [] 
  for i in range(nb):
    b.append(ExprAsInt("*((uint8_t*)(0x%x))" % (addr+i)))
  return b

def writeBytes(b, addr):
  for i in range(len(b)):
    gdb.execute("set *((uint8_t*)(0x%x)) = 0x%x" % (addr+i,b[i]))



TIMES_HIT = 0
FAULT_COL = 0 # Faulty column 
KEY_COLLECTION = [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]
RUN_WITH_FAULTS = False
RESULT = { 'correct': [], 'faulty':[] }



def run(inpt):
  global TIMES_HIT
  TIMES_HIT = 0
  gdb.execute("run "+inpt,False)
    

def hitBlob(brks,eip):
  global TIMES_HIT
  global FAULT_COL
  global RUN_WITH_FAULTS

  TIMES_HIT += 1
  print("HIT --> "+str(TIMES_HIT))
  if TIMES_HIT == (4*8 + FAULT_COL): # Before 9th round
    if RUN_WITH_FAULTS:
      # Inject fault
      print("inject fault")
      state_p = ExprAsInt("*((void**)($rbp-0x50))") # Get pointer to the state
      fault = [ random.randrange(0,0x100) ]  
      writeBytes(fault, state_p + 4*FAULT_COL)



def getResult(brks,eip):
  global RUN_WITH_FAULTS
  global RESULT

  print("get result")
  state_p = ExprAsInt("*((void**)($rbp-0x50))")
  if RUN_WITH_FAULTS:
    RESULT['faulty'] = readBytes(16,state_p)
  else:
    RESULT['correct'] = readBytes(16,state_p)
  print(RESULT)

def updateKeyCollection():
  global FAULT_COL
  global RESULT
  global KEY_COLLECTION

  if FAULT_COL == 0:
    indexes = [ 0, 7, 10, 13]
  elif FAULT_COL == 1:
    indexes = [ 1, 4, 11, 14]
  elif FAULT_COL == 2:
    indexes = [ 2, 5, 8, 15]
  elif FAULT_COL == 3:
    indexes = [ 3, 6, 9, 12]
 
  for i in indexes:
    summ_outputs = RESULT['correct'][i] ^ RESULT['faulty'][i]
    # Find all couples a,b so that a ^ b == summ_outputs
    for a in range(0x100):
        b = a ^ summ_outputs
        incKey(i, RESULT['correct'][i] ^ a)
        incKey(i, RESULT['correct'][i] ^ b)
        
def incKey(i, k):
  global KEY_COLLECTION
  if k in KEY_COLLECTION[i]:
    KEY_COLLECTION[i][k] += 1
  else:
    KEY_COLLECTION[i][k] = 1


def start(): 
  global FAULT_COL
  global RUN_WITH_FAULTS
  global RESULT
  global KEY_COLLECTION

  n_faults = 3
  for FAULT_COL in range(4):
    for i in range(n_faults):
      inpt = randInput()
      inpt = "A"*16
      print("-"*10 + " Running with "+inpt)
      RUN_WITH_FAULTS = False
      run(inpt) 
      RUN_WITH_FAULTS = True
      run(inpt) 
      print("Col: %d Fault: %d" % (FAULT_COL,i))
      printBytes(RESULT['correct'])
      printBytes(RESULT['faulty'])
      updateKeyCollection()
  print(KEY_COLLECTION)




SetBP(0x0046373e,hitBlob)
SetBP(0x00463cda,getResult)
start()
