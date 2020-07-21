#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   day3-2.py
@Time    :   2020/07/15 14:24:54
@Author  :   Snow 
@Version :   1.0
@Contact :   1419517126@qq.com
@License :   (C)Copyright 2020-2021, Snow
@Desc    :   demo
'''

# here put the import lib

'''
    日期时间
'''
import datetime
'''
    表示一段时间：2天6小时
    datetime中timedelta
'''
from datetime import timedelta
a = timedelta(days=2,hours=6)
b = timedelta(hours=4.5)
c = a+b
# print(c.days)
# print(c.seconds)
# print(c.seconds/3600)
# print(c.total_seconds())
# print(c.total_seconds()/3600)

'''
    表示指定时间
'''
from datetime import datetime
a= datetime(2020,2,24)
#datetime自动处理闰年
# print(a+timedelta(days=5))
#到今天，经过多长时间
b = datetime(2020,7,15)
c = b-a
# print(c.days())
now = datetime.today()
now+timedelta(minutes=8)



'''
    基本的时间和日期处理，用datetime
    处理时区的问题,模糊时间范围，节假日计算用dateutil模块
    ，方法dateutil.relativedelta()
'''
from datetime import datetime
from datetime import timedelta

a = datetime(2020,7,15)
# print(a + timedelta(months=1))
#报错：TypeError: 'months' is an invalid keyword argument for __new__()

#模糊时间范围：整月的间隔
from dateutil.relativedelta import relativedelta
b = a+relativedelta(months=1)
c = a+relativedelta(months=-1)
d = b-c
# print(d.days)


'''
    计算距离今天（周三）最近的一个周五出现的日期
    第一步：时间转换成星期几
'''
from datetime import datetime
from datetime import timedelta

weekdays = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
def pre_day(dayname,start_date=None):
    if start_date is None:
        start_date = datetime.today()
    #得到今天是星期几
    day_num = start_date.weekday()
    day_num_target = weekdays.index(dayname)

    days_ago = 7+day_num - day_num_target
    target_date = start_date - timedelta(days=days_ago)
    return target_date

result = pre_day('星期三')


'''
    求当前月份的日期范围
    第一步：得到当前月份的第一天
'''
from datetime import date,datetime,timedelta
import calendar
#计算当前月份的第一天和最后一天，并返回日期
def get_month_range(start_date=None):
    if start_date is None:
        #计算当前月份的第一天
        start_date = date.today().replace(day=1)
    _,days_in_month = calendar.monthrange(start_date.year,start_date.month)  
    end_date = start_date + timedelta(days=days_in_month)
    return (start_date,end_date)
one_day = timedelta(days=1)
first_day,last_day = get_month_range()   
while first_day < last_day:
    print(first_day)
    first_day +=one_day
# print(date.today().replace(day=1))

'''
    假设全世界都要高考，计划于7月7号和7月8号早上9:30在北京举行，
    要求全世界参加高考的同学同一时间参加，计算出在美国纽约参加考试的时间
 
    结合时区
    所有涉及到时区相关的问题, 都使用pytz 模块，这个包提供了Olson时区数据库，
    这个数据库是时区信息事实上的标准
'''
from datetime import datetime,timedelta
from pytz import timezone
import pytz
date1 = datetime(2020,3,8,1,45,0)
print(date1)
new_york = timezone('America/New_York')
new_york_local = new_york.localize(date1)
new_york_later = new_york.normalize(new_york_local+timedelta(minutes=30))
print(new_york_local)
print(new_york_later)  # 并没有考虑到夏令时的问题
# 使用UTC，一旦转换成了UTC，就不用考虑夏令时的问题了
utc_date = new_york_local.astimezone(pytz.utc)
later_utc = utc_date + timedelta(minutes=30)
print(utc_date)
print(later_utc)

'''
    时区，去ISO 3166国家代码 去查询pytz.county_timezones
'''
print(pytz.country_timezones('CN'))


import pytz
from datetime import datetime,timedelta
a = datetime(2020,7,6,9,30,0)
print(a)
#查看时区
name = pytz.country_timezones('cn')
name2 = pytz.country_timezones('us')
#设置时区对象
tz = pytz.timezone('America/New_York')
#生成带时区的时间时，一定要使用timezone.localize()来生成
newyork_time = tz.localize(a)
#设置utc世界标准时间
utc = pytz.utc
#astimezone(utc)将时间转为utc标准时间
b = newyork_time.astimezone(utc)
print(b)
#对于有用了夏时制的,要使用normzlize来处理
newyork_time2 = tz.normalize(newyork_time+timedelta(minutes=30))
newyork_time3 = tz.normalize(b)
