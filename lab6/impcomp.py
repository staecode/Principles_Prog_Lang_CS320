# Imp compiler (to stack machine SM)
#
# Usage: linux> ./python3 impcomp.py 
#        ...<type input here>...
#        ^D
#

# Imp - an imperative expression language:
#
#   Expr -> num                   # integer    
#        |  var                   # string 
#        |  (Op Expr Expr)        # binop     
#        |  (:= var Expr)         # assign     
#        |  (print Expr)          # output     
#        |  (seq Expr Expr)       # sequence      
#        |  (if Expr Expr Expr)   # if-stmt    
#        |  (while Expr Expr)     # while-loop  
#   Op   -> + | - | * | / | < | =
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
from sexpr import *
import sm

# iterator for new labels
def labelgen():
    label = 100
    while True:
        label += 1
        yield str(label)
newlab = labelgen()

# the main compiler function
# - e is an Imp program in nested list form
def comp(e):
    # e is an atom
    if type(e) is str:
        if e.isdigit():
            return 'PUSH ' + e
        return 'LOAD ' + e
    # e is a list
    assert type(e) is list, "Invalid exp form " + str(e)
    key = e[0]
    # bin-op (op e1 e2)
    if key in ('+', '-', '*', '/', '<', '='):
        code = comp(e[1]) + '; ' + comp(e[2])
        if key == '+':  return code + '; ADD'
        if key == '-':  return code + '; PUSH -1; MUL; ADD'
        if key == '*':  return code + '; MUL'
        if key == '/':  return code + '; DIVREM; POP'
        if key == '<':  return code + '; LE'
        if key == '=':  return code + '; EQ'
    # assign (:= x e)
    if key == ':=':
        return comp(e[2]) + '; DUP; STORE ' + e[1]
    # output (print e)
    if key == 'print':
        return comp(e[1]) + '; DUP; PRINT'
    # sequence (seq e1 e2)
    if key == 'seq':
        return comp(e[1]) + '; POP; ' + comp(e[2])
    # if-stmt (if c t f)
    if key == 'if':
        lab0 = next(newlab)
        lab1 = next(newlab)
        return comp(e[1]) + '; JUMPZ ' + lab0 + '; ' \
             + comp(e[2]) + '; JUMP ' + lab1 + '; LABEL ' + lab0 + '; ' \
             + comp(e[3]) + '; LABEL ' + lab1 
    if key == 'while':
        lab0 = next(newlab)
        lab1 = next(newlab)
        return 'LABEL ' + lab0 + '; ' + comp(e[1]) + '; JUMPZ ' + lab1 \
             + '; ' + comp(e[2]) + '; POP; JUMP ' + lab0 \
             + '; LABEL ' + lab1 + '; PUSH 0' 
    raise Exception("Illegal exp: " + str(e))

if __name__ == "__main__":
    prog = sys.stdin.read()
    lst = sexpr(prog)
    code = comp(lst)
    print(code)
