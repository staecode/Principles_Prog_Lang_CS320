#------------------------------------------------------------------------------ 
# For CS320 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

# convert an S-expression in string form to nested list form
# i.e. '(+ a (* b c))' => ['+', 'a', ['*', 'b', 'c']]
# (note: singletons stay the same: 'a' => 'a')
def sexpr(str):
    lst = str.replace('(', ' ( ').replace(')', ' ) ').split()
    if len(lst) == 1:
        return lst[0]
    stack = []
    for x in lst:
        if x == '(':
            stack.append([])
        elif x == ')':
            if len(stack) > 1:
                r = stack.pop()
                stack[-1].append(r)
        else:
            stack[-1].append(x)
    assert len(stack) == 1
    return stack.pop()

if __name__ == "__main__":
    print(sexpr('(+ a (* b c))'))
    print(sexpr('x'))    
