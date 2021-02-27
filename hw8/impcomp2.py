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

class Expr: 
    def labelgen():
        label = 100
        # because of yield, when function gains control 
        # again it will begin at while loop
        while True:
            label += 1
            yield str(label)
    # when next() called, will generate new yield
    newlab = labelgen()

class Num(Expr): 
    def __init__(self, val):
        self.val = val
    def comp(self):
        return "PUSH " + self.val

class Var(Expr): 
    def __init__(self, val):
        self.val = val
    def comp(self):
        return "LOAD " + self.val

class BinOp(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.result = left.comp() + "; " + right.comp()


class Add(BinOp):
    def __init__(self, left, right):
        super(Add, self).__init__(left, right)

    def comp(self):
        return self.result + "; ADD"
        
class Sub(BinOp): 
    def __init__(self, left, right):
        super(Sub, self).__init__(left, right)

    def comp(self):
        return self.result + "; PUSH -1; MUL; ADD"

class Mul(BinOp): 
    def __init__(self, left, right):
        super(Mul, self).__init__(left, right)

    def comp(self):
        return self.result + "; MUL"

class Div(BinOp): 
    def __init__(self, left, right):
        super(Div, self).__init__(left, right)
    
    def evel(self):
        return self.result + "; DIVREM; POP"

class Le(BinOp): 
    def __init__(self, left, right):
        super(Le, self).__init__(left, right)

    def comp(self):
        return self.result + "; LE"

class Eq(BinOp):
    def __init__(self, left, right):
        super(Eq, self).__init__(left, right)

    def comp(self):
        return self.result + "; EQ"

class Assign(Expr):
    def __init__(self, var, val):
        self.var = var
        self.val = val

    def comp(self):
        return self.val.comp() + "; DUP" \
            + "; STORE " + self.var.comp()

class Print(Expr):
    def __init__(self, val):
        self.val = val

    def comp(self):
        return self.val.comp() + "; DUP; PRINT"

class Seq(Expr):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def comp(self):
        return self.first.comp() + "; POP; " + self.second.comp()

class If(Expr):
    def __init__(self, condition, true, false):
        self.cond = condition
        self.true = true
        self.false = false

    def comp(self):
        lab1 = next(self.newlab)
        lab2 = next(self.newlab)
        return self.cond.comp() + "; JUMPZ " + lab1 + "; " \
            + self.true.comp() + "; JUMP " + lab2 \
            + "; LABEL " + lab1 + " " \
            + self.false.comp() + "; LABEL " + lab2

class While(Expr):
    def __init__(self, condition, statement):
        self.cond =  condition
        self.state = statement

    def comp(self):
        lab1 = next(self.newlab)
        lab2 = next(self.newlab)
        return "LABEL " + lab1 + " " + self.cond.comp() \
            + "; JUMPZ " + lab2 \
            + "; " + self.state.comp() \
            + "; POP; JUMP " + lab1 \
            + "; LABEL " + lab2 \
            + "; PUSH 0"

# convert input list to an ast
def ast(lst): 
    if len(lst) > 4:
        raise Exception("List length exceeds "\
            "available operations of language.")
    if not isinstance(lst, list):
        if lst.isnumeric():
            return Num(lst)
        else:
            return Var(lst)
    else:
        expr = None
        op = lst[0]
        if op == "+":
            expr = Add(ast(lst[1]), ast(lst[2]))
        elif op == "-":
            expr = Sub(ast(lst[1]), ast(lst[2]))
        elif op == "*":
            expr = Mul(ast(lst[1]), ast(lst[2]))
        elif op == "/":
            expr = Div(ast(lst[1]), ast(lst[2]))
        elif op == "<":
            expr = Le(ast(lst[1]), ast(lst[2]))
        elif op == "=":
            expr = Eq(ast(lst[1]), ast(lst[2]))
        elif op == ":=":
            expr = Assign(ast(lst[1]), ast(lst[2]))
        elif op == "print":
            expr = Print(ast(lst[1]))
        elif op == "seq":
            expr = Seq(ast(lst[1]), ast(lst[2]))
        elif op == "if":
            expr = If(ast(lst[1]), ast(lst[2]), ast(lst[3]))
        elif op == "while":
            expr = While(ast(lst[1]), ast(lst[2]))
        else:
            raise Exception("Operation not in language")

    return expr

if __name__ == "__main__":
    prog = sys.stdin.read()
    lst = sexpr(prog)
    tr = ast(lst)
    code = tr.comp()
    print(code)

