#------------------------------------------------------------------------------ 
# <PUT YOUR NAME HERE>
#------------------------------------------------------------------------------ 

# Imp compiler (to stack machine SM) version 2: OO style
#
# Usage: linux> ./python3 impcomp2.py 
#        ...<type input here>...
#        ^D

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
import sys
from sexpr import *
import sm

class Expr: pass 
class Num(Expr): pass
class Var(Expr): pass
class BinOp(Expr): pass
class Add(BinOp): pass
class Sub(BinOp): pass
class Mul(BinOp): pass
class Div(BinOp): pass
class Le(BinOp): pass
class Eq(BinOp): pass
class Assign(Expr): pass
class Print(Expr): pass 
class Seq(Expr): pass
class If(Expr): pass
class While(Expr): pass

# convert input list to an ast
def ast(lst): pass

if __name__ == "__main__":
    prog = sys.stdin.read()
    lst = sexpr(prog)
    tr  = ast(lst)
    code = tr.comp()
    print(code)
