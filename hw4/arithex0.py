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
        term()
        while next() == '+' or next() == '-':
            advance()
            term()
            
    # term -> factor {('*'|'/') factor}
    def term():
        factor()
        while next() == '*' or next() == '/':
            advance()
            factor()

    # factor -> '-' factor | '(' exp ')' | num
    def factor():
        if next() == '-':
            advance()
            factor()
        elif next() == '(':
            advance()
            exp()   
        else:
            c = next()
            if not c.isdigit():
                raise Exception("expected a number, got " + c)
            while next().isdigit() or next() == ')':
                advance()
            
    # parsing starts here
    exp()
    if i < len(str):
        raise Exception("found extra chars: " + str[i:])
    print("OK")   # parsing successful

if __name__ == "__main__":
    parse('12 + (4 * 2 - 5)')
    eval('12 + (4 * 2 - 5)')
    parse('12 + 2 * (10 - - 4 / 2) + 6')
    eval('12 + (4 * 2 - 5)')
    # below are error cases; should test each one separately
    # parse('x')      
    # parse('1=2')   
    # parse('1++2')   
    # parse('(1+2')   
    # parse(sys.argv[1])

