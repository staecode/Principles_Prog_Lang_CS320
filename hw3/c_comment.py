# CS320 Winter 2021 @PSU
# Program: c_comment(str) program for string validation of successful comment
# Author: Staci Harding
# Date: 1/23/2021

# test function to confirm results (str1) of the function
# match the expected (str2) value
def test_comment(str1, str2) :
    if(str1 == str2) :
        return 'SUCCESS'
    else:
        return 'FAILURE'

# simple comment validation, strips off any whitespace and then checks from and 
# back of string for expected /* and */
def c_comment(str) :
    clean_str = str.strip()
    if((clean_str[0:2] == '/*') and (clean_str[(len(clean_str)-2): len(clean_str)] == '*/')) :
        return 'TRUE'
    else :
        return 'FALSE'

# test various strings for whether they are comments
# pass results through comparison testing function
if __name__ == '__main__':
    print(test_comment(c_comment('/**/'), 'TRUE'))
    print(test_comment(c_comment('/*dgdfsg*/'), 'TRUE'))
    print(test_comment(c_comment('    /**/  '), 'TRUE'))
    print(test_comment(c_comment('/*dgdfsg     */   '), 'TRUE'))
    print(test_comment(c_comment('f/**/'), 'FALSE'))
    print(test_comment(c_comment('/**/f'), 'FALSE'))
    print(test_comment(c_comment('/f**/'), 'FALSE'))
    print(test_comment(c_comment('/**f/'), 'FALSE'))