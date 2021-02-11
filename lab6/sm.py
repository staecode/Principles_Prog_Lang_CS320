#------------------------------------------------------------------------------ 
# For CS320 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

# Stack Machine SM Interpreter
#
# Usage: linux> ./python3 sm.py
#        ...<type input here>...
#        ^D
# 
# SM - an stack machine:
#
#   PUSH  n   push constant n to stack
#   LOAD  x   load vars[x] to stack
#   STORE x   store val to vars[x]
#   ADD       val1 + val2, push result to stack
#   MUL       val1 * val2, push result to stack
#   DIVREM    val1 / val2, push div and rem results to stack 
#   LE        val1 < val2, push 1 (if true) or 0 (if false) to stack
#   EQ        val1 == val2, push 1 (if true) or 0 (if false) to stack
#   POP       pop off val
#   DUP       replicate val
#   SWAP      swap val1 and val2
#   PRINT     print val
#   LABEL i   nop, marking a label position in program
#   JUMP  i   branch to Label i
#   JUMPZ i   if val == 0 branch to Label i
#
import sys

debug = False

# turn on debug
def setdebug():
    global debug
    debug = True

def run(prog):
    vars = {}     # variable array
    stack = []    # operand stack
    labmap = {}   # label map
    pc = 0        # program counter

    def debug_msg(pc):
        print(pc, f'{prog[pc]:14}', 'vars:', vars, ' stack:', stack)

    # find all labels in program, map them to inst indices
    def build_labmap(prog):
        for idx in range(len(prog)):
            inst = prog[idx].split()
            if inst[0] == 'LABEL': 
                labmap[inst[1]] = idx
        if debug: print('>> labmap:', labmap)

    # execute one instruction (at position pc)
    def exec(pc):
        inst = prog[pc].split()
        cmd = inst[0]
        if cmd == '#':        # skip comments
            return pc + 1
        if cmd == 'PUSH':
            stack.append(int(inst[1]))
        elif cmd == 'LOAD':
            v = vars.get(inst[1])
            if not v:
                v = 0
            stack.append(v)
        elif cmd == 'STORE':
            v = stack.pop()
            vars[inst[1]] = v
        elif cmd == 'ADD':
            v2,v1 = stack.pop(),stack.pop()
            stack.append(v1+v2)
        elif cmd == 'MUL':
            v2,v1 = stack.pop(),stack.pop()
            stack.append(v1*v2)
        elif cmd == 'DIVREM':
            v2,v1 = stack.pop(),stack.pop()
            if v2 == 0:
                sys.exit("division by zero")
            stack.extend([v1//v2,v1%v2])
        elif cmd == 'LE':
            v2,v1 = stack.pop(),stack.pop()
            stack.append(1 if v1<v2 else 0)
        elif cmd == 'EQ':
            v2,v1 = stack.pop(),stack.pop()
            stack.append(1 if v1==v2 else 0)
        elif cmd == 'POP':
            stack.pop()
        elif cmd == 'DUP':
            v = stack.pop()
            stack.extend([v,v])
        elif cmd == 'SWAP':
            v2,v1 = stack.pop(),stack.pop()
            stack.extend([v2,v1])
        elif cmd == 'PRINT':
            v = stack.pop()
            print(v)
        elif cmd == 'JUMP':
            lab = inst[1]
            if debug: debug_msg(pc)
            return labmap[lab]
        elif cmd == 'JUMPZ':
            lab = inst[1]
            v = stack.pop()
            if not v:
                return labmap[lab]
        elif cmd == 'LABEL':
            pass
        if debug: debug_msg(pc)
        return pc + 1

    # interpretation starts here
    build_labmap(prog)
    while pc < len(prog):
        pc = exec(pc)
    if len(stack) > 1:
        raise Exception("Operand stack has more than one items")
    elif len(stack) == 0:
        raise Exception("Operand stack is empty")
    print("result:", stack[0])

if __name__ == "__main__":
    str = sys.stdin.read()
    if ';' in str:
        prog = str.split(';')     # single-line form
    else:
        prog = str.splitlines()   # multi-line form
    run(prog)
