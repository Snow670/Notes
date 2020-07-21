'''
    小数 
'''
'''
    小数的四舍五入round
    如果一个值刚好在两个边界的中间的时候，round函数返回离它最近的偶数
'''
result = round(1.2345,2)
print(result)
print(round(1.5))
print(round(2.5))

print(round(16754,-1))   #十位
print(round(16754,-2))   #百位
print(round(16754,-3))   #千位

'''
    decimal 定位数，牺牲性能
    对浮点数执行精确的计算操作，并且不能出现任何误差
    1.现实生活，很少能要求超过普通浮点数的17位精度
    2.原生浮点数计算要块的多
'''
print(1.2+2.4)

from decimal import Decimal
a = Decimal('4.2')
b = Decimal('2.1')
c = a+b
print(c)

print(2.1/1.3)
#小数点后50位，需要创建一个本地上下文并改变它的设置
from decimal import localcontext
with localcontext() as ctx:
    ctx.prec = 50
    print(2.1/1.3)

'''
    数字格式化输出，控制数字的：位数、对齐
'''
a = 1234.56789
print(format(a,'0.2f'))
#右对齐
print(format(a,'>10.1f'))
print(format(a,'<10.1f'))
print(format(a,'^10.1f'))
#千位分隔符
print(format(a,','))
#控制小数点后1位加上千位分隔符
print(format(a,',.1f'))
#科学计数法
print(format(a,'e'))
print(format(a,'0.2E'))

'''
    % 和 format 的区别
    % 不支持千位符
'''
'''
    字节字符串 -> 大整数
    大整数    -> 字节字符串
'''
data=b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
print(len(data))    #16位

#python中特有方法去转换  int.to_bytes()  int.from_bytes()
print(int.from_bytes(data,'little'))
print(int.from_bytes(data,'big'))
a=94522842520747284487117727783387188
print(a.to_bytes(16,'big'))

'''
    IPV6 网络地址使用一个128位的数字引擎
'''
'''
    正无穷，负无穷，NaN(非数字)
'''
a = float('inf')
b = float('-inf')
c = float('nan')
print(a)

#判断这几个值的存在，使用math.isinf()  math.isnan()
# nan == nan  判断结果为False
import math
print(math.isinf(a))
print(math.isinf(b))
print(math.isnan(c))

'''
    随机数random
'''
import random
list = [1,2,3,4,5,6]
#每次只产生一个随机数
print(random.choice(list))
#提取n个随机数
print(random.sample(list,3))
#打乱原顺序
print(random.shuffle(list))
print(list)
#生成随机整数 random.randint()
#生成0-1随机浮点数 random.random()
#获取N位随机位（二进制）的整数 random.getrandbits()
#1个byte字节 = 8个bit位
print(random.getrandbits(100))

# rand.seed()  rand.seed(1234) rand.seed(b'sgxh')