'''
    类：
    对象(实例)：
    面向过程编程VS面向对象编程
    面向对象的三大特征：封装，继承，多态
    单例模式（常见的23种设计模式当中最简单的一种）
    内存管理
    五子棋面向对象：分成几个类？  棋盘类，棋子类，判定类
    白棋下棋 -> 判定类 -> 黑棋下 -> 判定类 -> 黑或白赢 
'''
 
 
'''
    改变对象的字符串显示
'''
# class Car:
#     def getCarInfo(self):
#         print('车轮的个数：%d，颜色%s'%(self.wheelNum,self.color))
     
#     def move(self):
#         print('车正在移动...')
 
# BMW = Car()
# BMW.color = '黑色'
# BMW.wheelNum = 4
# BMW.move()
# BMW.getCarInfo()
 
 
# 要改变一个实例的字符串表示，可以重新定义它的: __str__()  和  __repr__()方法
# class Area:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#     def __str__(self):
#         return '({0.x!s},{0.y!s})'.format(self)
#     def __repr__(self):
#         return 'Area({0.x!r},{0.y!r})'.format(self)
 
# __repr__()方法返回一个实例的代码表示形式，通常用来重新构造这个实例
# __str__()方法将实例转换为一个字符串，使用str()或者print()函数会输出这个字符串 
# 如果__str__()没有被定义，就会使用__repr__()来替代
# 引用计数？自动引用计数
 
# a = Area(2,3)
# (2,3)  # __str__() 的输出结果
# Area(2,3)  # __repr__() 的输出结果
 
# print('a is {0!r}'.format(a))
# print('a is {0}'.format(a))
 
 
 
'''
    自定义format
'''
# _formats = {
#     'ymd' : '{d.year}--{d.month}--{d.day}',
#     'mdy' : '{d.month}--{d.day}--{d.year}',
#     'dmy' : '{d.day}--{d.month}--{d.year}'
# }
# class Date:
#     def __init__(self, year, month, day):
#         self.year = year
#         self.month = month
#         self.day = day
     
#     def __format__(self,code):
#         if code == '':
#             code = 'ymd'
#         fmt = _formats[code]
#         return fmt.format(d=self)
 
 
# d = Date(2020,7,20)
# print(format(d))
# print(format(d,'mdy'))
# print(format(d,'dmy'))
 
 
 
# from datetime import date
# d1 = date(2020,7,20)
# print(d1)
# print(format(d1,'%A,%B,%d,%Y'))
# print(format(d1,'%d %b %Y'))
 
 
'''
    内存管理，创建大量对象（上百万个）时候的内存管理
    每 BMW = Car() 都会在内存中开辟一块空间，大量的未被释放的对象就会占用很多的内存，这样程序就会特别吃内存
'''
# 给类添加 __slots__属性来极大的减少实例所占的内存
# 定义 __slots__属性后，Python就会为实例使用一种更加紧凑的内部表示。
# 实例通过一个很小的固定大小的数组来创建，而不是为每个实例定义一个字典，这跟元组或列表很类似
# 在 __slots__中列出的属性名在内部被映射到这个数组的指定小标上。
# 缺点：使用 __slots__属性后，不能再给实例添加新的属性，只能使用 __slots__中定义的属性名
# class Date:
#     __slots__ = ['year','month','day']
#     def __init__(self, year, month, day):
#         self.year = year
#         self.month = month
#         self.day = day
 
# class Date1:
#     def __init__(self, year, month, day):
#         self.year = year
#         self.month = month
#         self.day = day
 
# date = Date(2020,7,20)
# date1 = Date1(2020,7,20)
 
# # sys.getsizeof很棒,但很浅(例如,在列表中调用,它不包括列表元素占用的内存).
# # pip install pympler
# from pympler.asizeof import asizesof
# print(asizesof(date,asign=1))  # 148
# print(asizesof(date1))  # 432


'''
    类的属性和方法的保护，自定义访问控制
    在Java,类的属性和方法：私有private，保护protected，公有public
    Python中，通过遵循一定的属性和方法命名规约来达到这个效果。
    第一个约定：使用单下划线 _ 开头的名字都应该是内部实现
'''
 
# class A:
#     def __init__(self):
#         self._internal = 0 # 内部的
#         self.public = 1   # 公有的属性
 
#     def public_method(self):
#         # 公有方法
#         pass
     
#     def _internal_method(self):
#         pass
 
'''        
    第二个约定：使用双下划线 __ 开头的命名会导致访问名称变成其他形式
    私有属性会被重命名为: _B__private
    私有方法会被重命名为: _B__private_method
'''
# class B:
#     def __init__(self):
#         self.__private = 0
     
#     def __private_method(self):
#         pass
 
#     def public_method(self):
#         pass
#         self.__private_method()
 
 
# 写一个C类继承自B类
 
# class C(B):
#     def __init__(self):
#         super().__init__()
#          self.__private = 1  # 不能覆盖父类B中的self.__private = 0, C类中被重命名成了_C__private
     
#     def __private_method(self):  # 不能覆盖父类B中的__private_method(self) ，C类中被重命名成了 _C__private_method
#         pass
 
 
 
# _  大多数情况下，非公共名称应该以单下划线 _ 开头
# 子类继承的问题，父类中一些内部属性应该在子类中隐藏，最好使用双下划线 __
# 有时候你定义的一个变量和某个保留字，关键字冲突，这个时候可以使用单下划线作为后缀
lambda_ = 1.0
 
 
 
 
 
'''
    设置属性，访问属性都很容易，如果我想给这个实例的属性增加除了设置和访问之外的处理逻辑
    比如：类型检查，合法性验证
'''
# 需要用到 property
# 增加了一个属性简单的类型检查
# 设置了property，看上去和attribute没有区别，但是访问它的时候会自动触发getter，setter，deleter方法
 
# class Person:
#     def __init__(self, first_name):
#         self.first_name = first_name
     
#     # 设置getter方法
#     @property
#     def first_name(self):
#         return self._first_name
 
#     # 设置setter方法
#     @first_name.setter
#     def first_name(self, value):
#         if not isinstance(value,str):
#             raise TypeError('请输入字符串类型')
#         self._first_name = value
 
#     # 设置deleter方法
#     @first_name.deleter
#     def first_name(self):
#         raise AttributeError('不能删除这个属性')


# 在类初始化的时候做类型检查
 
# class Person:
#     def __init__(self, first_name):
#         self.set_first_name(first_name)
 
#     def get_first_name(self):
#         return self._first_name
 
#     def set_first_name(self,value):
#         if not isinstance(value,str):
#             raise TypeError('请输入字符串类型')
#         self._first_name = value
#     def del_first_name(self):
#         raise AttributeError('不能删除这个属性')
 
#     name = property(get_first_name,set_first_name,del_first_name)
         
 
# a = Person('Bruce')
# print(a.name)
# a.name = 400
# del a.name
 
# 一个property属性就是一系列相关绑定方法的集合
# print(Person.name.fget)
# print(Person.name.fset)
# print(Person.name.fdel)
 
 
 
# property 动态计算attribute的方法，这种属性不会被实际的存储，而是在需要的时候计算出来
import math
 
class Circle:
    def __init__(self, radius):
        self.radius = radius
 
    @property
    def area(self):
        return math.pi * self.radius**2
     
    @property
    def diameter(self):
        return self.radius*2
 
    @property
    def perimeter(self):
        return 2*math.pi * self.radius
     
 
c = Circle(4.0)
print(c.radius)
print(c.area)
print(c.perimeter)