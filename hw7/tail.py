# Assignment: CS320 f(x)
# Author: Staci Harding
# Description: alter example function 
# to remove tail recursion call
# Date: 2/19/2021

def f(x):
    if x > 100:
        return x - 10
    while x <= 100:
        x += 11
    x -= 10
    return f(x)
        
#    if x > 100:
#        return x - 10
#    else:
#        return f(f(x+11))


if __name__ == '__main__':
    num = 5
    print(f(num))
