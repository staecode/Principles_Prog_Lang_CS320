#------------------------------------------------------------------------------ 
# For CS320 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

# Interpreter and compiler for a simple boolean expression language.
#
#   Expr -> t                 // true
#        |  f                 // false
#        |  (not Expr)        // negation
#        |  (and Expr Expr)   // and
#        |  (or Expr Expr)    // or 
#        |  (xor Expr Expr)   // exclusive-or
#        |  (eq Expr Expr)    // equality comparison
#
import sys
from sexpr import *

# validate an AST (in list form)
def validate(n):
    # acceptable language characters
    accepted = ['t', 'f', 'not', 'and', 'or', 'xor', 'eq']
    for item in n: 
    # if item is list
        if(type(item) is list) :
            succ = validate(item) 
    # break validating routine and raise exception
        else :
            if item not in accepted:
                raise Exception('The entered expression contains \
characters not in this language')
            else: 
                succ = 'OK'
    # portion of list has made it through validation, return OK
    return succ
                
# recursively evalutate list form ast by tackling each embedded list
# return compounded results at scope
def eval_R(n):
    result = False
    op = n[0]
    if(op == 'not'):
        if(type(n[1] is list)):
            result = eval_R(n[1])
        else:
            result = True if n[1] == 't' else False
        return not result
    else:
        if(type(n[1]) is list):
            parm1 = eval_R(n[1])
        else:
            parm1 = True if n[1] == 't' else False
        if(type(n[2]) is list):
            parm2 = eval_R(n[2])
        else:
            parm2 = True if n[2] == 't' else False   
        if(op == 'and') :
            return parm1 and parm2
        elif(op == 'or'):
            return parm1 or parm2
        elif(op == 'xor'):
            return (parm1 and not parm2) or (not parm1 and parm2)
        elif(op == 'eq'):
            return parm1 == parm2
        # operation should not have made it through validation
        else:
            raise Exception('Cannot execute with: ' + op + ' ' + parm1 + ' ' + parm2)



# evaluate an AST (in list form)
# (not implementing short-circuit evaluation)
def eval(n):
    # pass to recursive evaluator
    result = eval_R(n)
    # return boolean result as string result
    return 'True' if result else 'False'

            

# compile an AST (in list form) to SM0 code
# (not implementing short-circuit evaluation)
# recursively build string by building stack equivalence at scope
def comp(n):
    # nothing embedded, return only
    if n == 't': return 'T '
    if n == 'f': return 'F '
    if len(n) == 2: 
        assert n[0] == 'not', "expected 'not', got " + n[0]
        result = comp(n[1]) + 'NOT '
    op = n[0]
    left = comp(n[1])   # left operand
    right = comp(n[2])  # right operand
    if op == 'and': 
        result = left + right + 'AND '
    elif op == 'or':  
        result = left + right + 'OR '
    elif op == 'xor': 
        result = left + right + 'NOT AND ' + left + 'NOT ' + right + 'AND OR ' 
    elif op == 'eq':  
        result = left + right + 'AND ' + left + 'NOT ' + right + 'NOT AND OR ' 
    else:
        raise Exception("expected an boolean op, got " + op)
    return result

if __name__ == "__main__":
#    str = sys.stdin.readline() # get the input from stdin
    str = sys.argv[1]          # get the input from command-line
    ast = sexpr(str)           # parse the input to ast
    print("Nested list: ", ast)
    print("Validating:  ", validate(ast))
    print("Interpreting:", eval(ast))
    print("Compiling:   ", comp(ast))
