# Assignment: CS320 twice(f, x)
# Author: Staci Harding
# Description: applies a function twice to a parm
# Date: 2/19/2021

def twice(f):
    return lambda a: f(f(a))

def func(parm):
    return 2 * parm

if __name__ == '__main__':
    num = 2
    print(twice(func)(num))

