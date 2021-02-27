# Assignment: CS320 power(f, x)
# Author: Staci Harding
# Description: apply a function to a parm x amount of time
# Date: 2/19/2021


def power(f, x):
    if(x == 0):
        return lambda a: a
    return lambda a: f(power(f, x - 1)(a))


def func(parm):
    return parm * 5 


if __name__ == '__main__':
    num = 5
    print(power(func, num)(num))
