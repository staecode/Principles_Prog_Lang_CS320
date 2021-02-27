# Assignment: CS320 mapL(r, iter)
# Author: Staci Harding
# Description: 
#   Modeled in the fashion of map(r, iter) but
#   instead returns a list, instead of a map object
# Date: 2/19/2021


def mapL(r, iter):
   res = []
   for item in iter:
       res.append((lambda x: r(x))(item))
   return res


def func(parm):
    return parm * 11

if __name__ == "__main__":
    my_list = [1,2,3,4]
    print(mapL(func, my_list))
    

    
