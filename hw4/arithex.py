#------------------------------------------------------------------------------ 
# Staci Harding
#------------------------------------------------------------------------------ 

# Arith Expr Parser (top-down)
#
# Grammar: (num is a terminal representing an integer)
#   exp    -> term {('+'|'-') term}
#   term   -> factor {('*'|'/') factor}
#   factor -> '-' factor 
#          |  '(' exp ')'
#          |  num
#
# Usage: linux> ./python3 arithex0.py 'arith exp'
#
import sys

# str is an input program, e.g. '12 + (4 * 2 - 5)'
def parse(str):
    i = 0  # idx to input string

    # lookahead next non-space char, return '$' if reaches the end
    def next():
        if i < len(str):
            while(str[i] == ' '):
                advance()
            return str[i]
        return '$'

    # advance the input idx
    def advance():
        nonlocal i
        i += 1

    # exp -> term {('+'|'-') term}
    def exp():
        ast = term()
        while next() == '+' or next() == '-':
            c = next()
            advance()
            ast = [c, ast, term()]
        return ast
            
    # term -> factor {('*'|'/') factor}
    def term():
        ast = factor()
        while next() == '*' or next() == '/':
            c = next()
            advance()
            ast = [c, ast, factor()]
        return ast

    # factor -> '-' factor | '(' exp ')' | num
    def factor():
        if next() == '-':
            advance()
            ast = ['-', factor()]
        elif next() == '(':
            advance()
            ast = exp()   
        else:
            c = next()
            start = i
            if not c.isdigit():
                raise Exception("expected a number, got " + c)
            while next().isdigit():
                advance()
            ast = str[start:i].strip()
            if next() == ')':
                advance()
        return ast
            
    # parsing starts here
    ast = exp()
    if i < len(str):
        raise Exception("found extra chars: " + str[i:])
    return ast

def eval(n):
    result = 1
    op = n[0]
    if(op == '-'):
        if len(n) == 2:
            result = int(n[1]) * (-1)
        else:
            if type(n[1]) is list:
                val1 = eval(n[1])
            else:
                val1 = int(n[1])
            if type(n[2]) is list:
                val2 = eval(n[2])
            else:
                val2 = int(n[2])
            result = val1 - val2
    else:   
        if type(n[1]) is list:
            val1 = eval(n[1])
        else:
            val1 = int(n[1])
        if type(n[2]) is list:
            val2 = eval(n[2])
        else:
            val2 = int(n[2])
        if(op == '+'):
            result = val1 + val2
        elif(op == '*'):
            result = val1 * val2
        elif(op == '/'):
            result = val1 / val2
        else:
            raise Exception ('Operator not recognized')
        
    return result



if __name__ == "__main__":
    my_string = '12 + (4 * 2 - 5)'
    print('Original String: ', my_string)
    ast = parse(my_string)
    print('AST: ', ast)
    print('Value: ', eval(ast))
    my_string = '12 + 2 * (10 - - 4 / 2) + 6'
    print('Original String: ', my_string)
    ast = parse(my_string)
    print('AST: ', ast)
    print('Value: ', eval(ast))

    # below are error cases; should test each one separately
    # parse('x')      
    # parse('1=2')   
    # parse('1++2')   
    # parse('(1+2')   
#   parse(sys.argv[1])
