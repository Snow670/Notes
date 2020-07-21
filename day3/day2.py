'''
    1. 用户身份验证
    输入用户名admin，密码123456，打印出登出成功，否则登录失败
'''
name = input('输入用户名：')
password = input('输入密码：')
if name == 'admin' and password == '123456':
    print('登录成功')
'''
    2. 百分制成绩转换成等级成绩，均不包含上边界
    > 90      A
    80-90     B
    70-80     C
    60-70     D
    < 60      E
'''
score = float(input('请输入成绩：'))
if score > 90:
    print('A')
elif 80 <= score < 90:
    print('B')
elif 70 <= score < 80:
    print('C')
elif 60 <= score < 70:
    print('D')
else:
    print('E')

'''
    3.输入三条边长，如果能构成三角形就计算其面积和周长
'''
import math
a = float(input('输入一条边a：'))
b = float(input('输入一条边b：'))
c = float(input('输入一条边c：'))
if a + b > c and a + c > b and b + c > a:
    print('周长为%f' % (a+b+c))
    p = (a + b + c) / 2
    area = math.sqrt(p * (p - a) * (p - b) * (p - c))
    print('面积: %f' % area)
else:
    print('不能构成三角形')