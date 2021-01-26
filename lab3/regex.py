#------------------------------------------------------------------------------ 
# For CS320 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

# RegEx Parser (top-down)
#
# Grammar: (c is a terminal representing a single letter)
#   e    -> alt
#   alt  -> seq {'|' seq}
#   seq  -> rep {rep}
#   rep  -> atom ['*']
#   atom -> '(' e ')' | c
#
# Usage: linux> ./python3 regex.py 'RE string'
#
import sys

def regex(str):
    i = 0  # idx to input string

    # lookahead the next char, return '$' if reaches the end
    def next():
        if i < len(str):
            return str[i]
        return '$'

    # match a char, advance the input idx
    def match(c):
        nonlocal i
        if str[i] == c:
            i += 1
        else:
            raise Exception("expected " + c + " got " + str[i])

    # alt -> seq {'|' seq}
    def alt():
        seq()
        while next() == '|':
            match('|')
            seq()
            
    # seq -> rep {rep}
    def seq():
        # ... add code here
        pass

    # rep -> atom ['*']
    def rep():
        # ... add code here
        pass
    
    # atom -> '(' alt ')' | c
    def atom():
        if next() == '(':
            match('(')
            alt()
            match(')')
        else:
            c = next()
            if not c.isalpha():
                raise Exception("expected a letter, got " + c)
            match(c)

    # parsing starts here
    # e -> alt
    alt()
    if i < len(str):
        raise Exception("found extra chars: " + str[i:])
    return True

if __name__ == "__main__":
    print(regex(sys.argv[1]))

