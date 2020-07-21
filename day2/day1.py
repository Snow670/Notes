'''
练习五：用户输入自己出生年月日，判断用户的星座和生肖
'''
chinese_zodiac = '猴鸡狗猪鼠牛虎兔龙蛇马羊'
star_name = ('摩羯座','水瓶座','双鱼座','白羊座','金牛座','双子座','巨蟹座','狮子座','处女座','天秤座','天蝎座','射手座')
star_days = ((1,20),(2,19),(3,21),(4,20),(5,21),(6,22),(7,23),(8,23),(9,23),(10,24),(11,23),(12,22))
year = int(input('请输入出生年：'))
month = int(input('请输入月份：'))
day = int(input('请输入日期：'))
index = year%12
num = len(list(filter(lambda x:x<(month,day),star_days)))
print('%d年%d月%d日的生肖和星座是%s-%s'%(year,month,day,chinese_zodiac[index],star_name[num]))
'''
for x in star_days:
 if x<(month,day):
  print(x)
f_list = filter(lambda x:x<(month,day),star_days)
new_list = list(f_list)
print(new_list)
num = len(new_list)
print(num)
print(star_name[num])
'''
'''
for num in range(len(star_days)):
 if star_days[num] > (month,day):
  print(star_name[num])
  break
 elif month==12 and day>22:
  print(star_name[0])
  break
'''
'''
num = 0
while star_days[num] < (month,day):
 if month==12 and day>22:
  break
 num +=1
print('出生于%d月%d日的星座是：%s'%(month,day,star_name[num]))
'''

'''
    1. 有四个数字：1,2,3,4,能组成多少个互不相同且无重复数字的三位数？输出这些数字
    2. 一个10000以内的整数，它加上100和加上268后都是一个完全平方数，请问该数是多少？
    3. 输入年月日，判断这一天是这一年的第几天
'''

'''
1.思路：因为是三位数，所以从1,2,3,4中取一个数，再从1,2,3,4中取一个数，再从1,2,3,4中取一个数，
然后取出的3个数组合成3位数，条件是取出的3个数字互不相等
'''
for i in range(1,5):
	for m in range(1,5):
		for n in range(1,5):
			if i != m and i !=n and m !=n:
				print('%d%d%d'%(i,m,n))
'''
2.思路：一个10000以内的整数i range(10000)  i+100=一个完全平方数m,i+268=一个完全平方数n
'''
import math
for i in range(10000):
	m = int(math.sqrt(i + 100))
	n = int(math.sqrt(i + 268))
	if m*m == i+100 and n*n == i+268:
		print(i)
'''
3. 输入年月日，判断这一天是这一年的第几天
闰年的2月份是29天，全年366天
平年的2月份是28天，全年365天
公历闰年判定遵循的规律为: 四年一闰,百年不闰,四百年再闰.
'''
year = int(input('请输入年份：'))
month = int(input('请输入月份：'))
day = int(input('请输入日期：'))
sum = 0
#平年每月的天数
a = [31,28,31,30,31,30,31,31,30,31,30,31]
#判断是否是闰年
if year % 4 ==0 and year % 100 !=0 or year % 400 ==0:
	a[1] = 29
#判断月份大小，根据下标获取对应的天数
for i in range(12):
	if month > i + 1:
		sum += a[i]
#总天数
sum = sum+day
print('这一天是%d年的第%d天' %(year,sum))

'''
练习六：用户输入多个出生年月日，判断用户的星座和生肖，统计每个生肖和星座人数
多次输入：while True
'''
chinese_zodiac = '猴鸡狗猪鼠牛虎兔龙蛇马羊'
star_name = ('摩羯座', '水瓶座', '双鱼座', '白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座')
star_days = (
(1, 20), (2, 19), (3, 21), (4, 20), (5, 21), (6, 22), (7, 23), (8, 23), (9, 23), (10, 24), (11, 23), (12, 22))

# {生肖：次数}
chinese_zodiac_dict = {}
for i in chinese_zodiac:
	chinese_zodiac_dict[i] = 0

# {星座：次数}
star_name_dict = {}
for m in star_name:
	star_name_dict[m] = 0

while True:
	year = int(input('请输入出生年：'))
	month = int(input('请输入月份：'))
	day = int(input('请输入日期：'))
	index = year % 12
	num = 0
	while star_days[num] < (month, day):
		if month == 12 and day > 22:
			break
		num += 1

	print('出生于%d年的生肖是：%s' % (year, chinese_zodiac[index]))
	print('出生于%d月%d日的星座是：%s' % (month, day, star_name[num]))

	chinese_zodiac_dict[chinese_zodiac[index]] += 1
	star_name_dict[star_name[num]] += 1

	for key in chinese_zodiac_dict.keys():
		print('生肖是%s的有%d个' % (key, chinese_zodiac_dict[key]))

	for key in star_name_dict.keys():
		print('星座是%s的有%d个' % (key, star_name_dict[key]))




