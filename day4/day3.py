'''
    函数实现计算两数的最大公约数和最小公倍数
'''
def gcd(x,y):
    # 保证小的数在前面
    # if x >y:
    #     a = x
    #     x = y
    #     y = a
    # Python中特有的方式
    if x<y:
        x,y = y,x
    #Python中三步运输
    # (x,y = y,x) if x>y else (x,y)
    for i in range(2,y+1):
        if x%i == 0 and y%i == 0:
            max = i
    min = (x*y)/max
    print("最大公约数为:%d" % max)
    print("最小公倍数为:%d" % min)

# gcd(12,8)
'''
    判断一个数是不是回文数
    回文数是指正读（从左往右）和反读（从右往左）都一样的一类数字，例如：12321、1221等。
'''
def is_palindrome(num):
    temp = num   #121
    total = 0
    while temp > 0:
        total = total * 10 + temp % 10  #
        temp //= 10
    print(num, total)
    return total == num
# print(is_palindrome(121))
# if __name__ == "__main__":
#     num = int(input("请输入一个正整数，num = "))
#     if is_palindrome(num):
#         print("%d 是回文数！" % num)
#     else:
#         print("%d 不是回文数！" % num)

'''
    判断一个数是不是素数
'''
def is_num(num):
    flag = True
    for i in range(2,num):
        if num%i == 0:
            flag = False
            return flag
    return flag if num!=1 else False

# print(is_num(3))

'''
    leetCode 866 回文素数
'''
def is_pnum(num):
    temp = num
    total = 0
    while temp > 0:
        total = total * 10 + temp % 10  #
        temp //= 10
    # print(num, total)
    if total == num:
        flag = True
        for i in range(2, num):
            if num % i == 0:
                flag = False
                return flag
        return flag if num != 1 else False
# if __name__ == "__main__":
#     num = int(input("请输入一个正整数，num = "))
#     if is_pnum(num):
#         print("回文数%d是素数" % num)
#     else:
#         print("回文数%d不是素数" % num)