#------------------------------------------------------------------------------ 
# For CS320 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

# Stack Machine SM0 Interpreter
#
# SM0 instructions: T, F, NOT, AND, OR
#
# Usage: ./python3 sm0.py 'program string'
#
import sys

# execute prog (a list of commands)
def exec(prog):
    stack = []    # operand stack
    for cmd in prog:
        if   cmd == 'T': stack.append(True)
        elif cmd == 'F': stack.append(False)
        elif cmd == 'NOT':  
            v1 = stack.pop()
            stack.append(not v1)
        elif cmd == 'AND':
            v2 = stack.pop()
            v1 = stack.pop()
            stack.append(v1 and v2)
        elif cmd == 'OR':
            v2 = stack.pop()
            v1 = stack.pop()
            stack.append(v1 or v2)
    if len(stack) != 1:
        raise Exception("Wrong #items on stack ", stack)
    return stack[0]

if __name__ == "__main__":
#    str = sys.stdin.readline()
    str = sys.argv[1]
    print(exec(str.split()))

    
