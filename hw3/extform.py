# CS320 Winter 2021 @PSU
# Program: extform(lst) program for producing S.Expression of AST from list form
# Author: Staci Harding
# Date: 1/23/2021

# test function to confirm results (str1) of the function
# match the expected (str2) value
def test_Sexpr(str1, str2) :
    if(str1 == str2) :
        return 'SUCCESS'
    else:
        return 'FAILURE'

# convert a list form ast to an S.expression
def extform(lst) :
    # if the parm is just a string, return it as list item
    if(isinstance(lst, str)) :
        return lst
    # else build a new string S.expression for returning,
    # build from the list items available in scope
    new_str = '('
    for item in lst :
        # if a new list was found embedded in this list, recursive call
        # to this function for further string production, append result 
        # to end of current string
        if (type(item) is list) :
            new_str = new_str + extform(item)
        else :
        # else build the string from the string item in list
            new_str = new_str + item + ' '
    # strip the extra whitespace on end (created by skipping testing in else)
    new_str = new_str.strip()
    # add paren to close this portion of S.expression
    new_str = new_str + ')'
    # return string built at this point
    return new_str

# convert ast lists to S.expression
# pass results through comparison testing function
if __name__ == '__main__':
    lst = ['+', 'a', ['*', 'b', 'c']]
    print(test_Sexpr(extform(lst), '(+ a (* b c))'))
    lst = 'atom'
    print(test_Sexpr(extform(lst), 'atom'))
    lst = ['alt', ['seq', 'a', 'b'], ['rep', 'c']]
    print(test_Sexpr(extform(lst), '(alt (seq a b)(rep c))'))
 