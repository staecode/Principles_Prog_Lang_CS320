# CS320 Winter 2021 @PSU
# Program: regex_to_ast.py program for producing ast in nested list form from RE
# Author: Staci Harding
# Date: 1/23/2021


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
        # get results of first sequence test
        ast = seq()
        while next() == '|':
            match('|')
            # if there is or option, build list item with 'alt',
            #  ast returned earlier, next sequence test
            ast = ['alt', ast, seq()]
        # return list built in while loop OR (in case of non alt)
        # then only return the results of seq()
        return ast
            
    # seq -> rep {rep}
    def seq():
        # get results of first repetition test
        ast = rep()
        while next() == '(' or next().isalpha():
            # if there is continued character seq, build
            # ast with 'seq', ast returned earlier, next
            # repition test
            ast = ['seq', ast, rep()]
        # return list built in while loop OR (in case of non seq)
        # then only return the results of rep()
        return ast

    # rep -> atom ['*']
    def rep():
        # get results of character test (new item or ch)
        ast = atom()
        if next() == '*':
            match('*')
            # if there is repetition option, build
            # ast with 'rep', ast returned earlier
            # that includes multiple possible list 
            # items from the alt() call in the atom() function
            ast = ['rep', ast]
        # return list built in if OR (in case of no rep)
        # then only return the results of atom()
        return ast
    
    # atom -> '(' alt ')' | c
    def atom():
        if next() == '(':
            match('(')
            # if new item, need new test of next piece of string
            # pass it through starting parse function alt() and
            # catch the results of the next item in ast list form
            ast = alt()
            match(')')
        else:
            c = next()
            if not c.isalpha():
                raise Exception("expected a letter, got " + c)
            match(c)
            # only a character remains in this stack, return that character
            ast = c
        # return either results of another item/token test or return
        # simply a character that was found as terminal
        return ast

    # parsing starts here
    # e -> alt
    ast = alt()
    if i < len(str):
        raise Exception("found extra chars: " + str[i:])
    return ast

# results printed in testing, for reading in the terminal (as I am still needing to map through the 
# parser with each input and confirm I've gotten the correct results for what I decided to test)
if __name__ == "__main__":
    print('Converting xy*|z to ast: ', regex('xy*|z'))
    print('Converting xyz*|z to ast: ', regex('xyz*|z'))
    print('Converting x*|zzzzzz to ast: ', regex('x*|zzzzzz'))
    print('Converting xz*xx to ast: ', regex('xz*xx'))


