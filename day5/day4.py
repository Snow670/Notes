'''
数据格式：txt html csv json xml base64
    csv   约等于 excel
    JSON  轻量级的数据格式，key-value,体积小，速度快
    XML   标签<book>hello</book>,体积大，速度慢
    base64   压缩图片
'''


'''
    csv
'''
import csv

#list 列表
with open('day4-0.csv',encoding='utf8') as f:
    f_csv = csv.reader(f)
    head = next(f_csv)
    print(head)
    #row 是列表格式  
    for row in f_csv:
        print(row)
    
#namedtuple 命名元组
from collections import namedtuple

with open('day4-0.csv',encoding='utf8') as f:
    f_csv = csv.reader(f)
    #获取csv头
    headings = next(f_csv)
    print(headings)
    #映射名称到序列元素
    Row = namedtuple('Row',headings)
    for r in f_csv:
        row = Row(*r)
        print(row.name)


# dict 字典
with open('day4-0.csv',encoding='utf8') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        print(row['name'])
        print(row['price'])


'''
    写入csv
'''
#设置表头
headers = ['name','price']
rows = [
    ('橘子',400),
    ('西瓜',300)
]
with open('day4-0.csv','a',encoding='utf8') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)


#写入的数据格式是dict
headers = ['name','price']
rows = [
    {
        'name':'橘子',
        'price':400
    },
    {
        'name':'西瓜',
        'price':300
    }
]
with open('day4-0.csv','w',encoding='utf8') as f:
    f_csv = csv.DictWriter(f,headers)
    f_csv.writeheader()
    f_csv.writerows(rows)

#分割符不都是逗号，可以是\t
#list 列表
with open('day4-0.csv',encoding='utf8') as f:
    f_csv = csv.reader(f,delimiter='\t')
    print(head)
    #row 是列表格式
    for row in f_csv:
        print(row)