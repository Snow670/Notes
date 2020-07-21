'''
    从XML文件中提取数据
    在java或者Android开发中常用
    html 超文本标记语言
'''
'''
    使用xml.etree.ElementTree 模块从简单的文档中提取数据
'''

from xml.etree.ElementTree import parse

file_path = './day5-1.xml'
#该元素是已解析树的根元素
doc = parse(file_path)

# root = doc.getroot()
# print(root.tag)
# for child in root:
#     print(child.tag,child.attrib)

# for unit in doc.iterfind('units/unit'):
#     print(unit.findtext('title'))


'''
    https://www.tripadvisor.cn/Attractions-g298557-Activities-oa30-Xi_an_Shaanxi.html#FILTERED_LIST
    获取景点数据
    两个第三方库：beautifulsoup4  解析请求过来的网络数据
                requests       网络请求
    一个xml或者html解析库：lxml
'''
import requests
from bs4 import BeautifulSoup
from lxml import etree

#爬取多页数据
urls = ['https://www.tripadvisor.cn/Attractions-g298557-Activities-oa{}-Xi_an_Shaanxi.html#FILTERED_LIST'.format(str(i)) for i in range(0,120,30)]
# # 从网站请求数据
for url in urls:
    print(url)
    web_data = requests.get(url)
    # 使用bs4和lxml引擎进行解析
    soup = BeautifulSoup(web_data.text,'lxml')
    titles = soup.select('div > div > div > div.listing_info > div.listing_title > a')
    tips = soup.select('div > div > div > div.listing_info > div.listing_rating > div:nth-child(2) > div > span.more > a')
    imgs = soup.select('div > div > div > div.photo_booking.non_generic > a > img')

    for title, tip, img in zip(titles, tips, imgs):
        print(title.get_text())
        print(tip.get_text())
        print(img.get('src'))


print('-------------------------------')
html_obj = etree.HTML(data.text)
#给元素定位，获取所有的元素  xpath('//p')获取所有的p标签
result = html_obj.xpath('//*')
print(html_obj)

'''
    爬虫分成4个等级：
        1.从API爬取
        2.从本地网站爬取
        3.从网络网站爬取
        4.从APP爬取，微信是最难的 vue,react (SPA singlee page application 单页单页应用) 
'''

'''
    上午总结：
    xml   简单的数据
    1. 如果提取的是比较简单的xml数据，就可以使用xml, xml.tree.ElementTree.parse()函数解析整个xml文档
       然后使用find(),iterfind()和findtext()等方法来搜索特定的XML元素，这些函数的参数就是标签名
    2. doc = parse(file_path)  doc.iterfind('units/unit')
    3. e.tag 标签名，e.attrib  属性  e.text 内部文本  get()方法可以获取属性值

    lxml  复杂大型的数据
    1. from lxml.etree import parse
'''

'''
    str1 = '<html><p>这是一段文字</html>'
    # 支持html的，可以自动补全的
    etree.HTML 
    # 支持xml，xml不允许有单标记的   
    etree.fromstring
'''
# from lxml import etree

# str1 = '<html><p>这是一段文字</p></html>'

# # str 转换成 xml,html 格式
# data_xml = etree.fromstring(str1)
# print(data_xml)

# # 把data_xml转换成str
# data_str = etree.tostring(data_xml,encoding=str,pretty_print=True)
# print(data_str)

# from lxml import etree

# str1 = '<html><p>这是一段文字</html>'
# data_html = etree.HTML(str1)
# # data_xml = etree.fromstring(str1)

# print(data_html)
# print('--------------------')
# print(data_xml)




'''
    解析大型的复杂的XML文件
    小目标：尽可能少使用内存从超大的XML文档中提取数据
    解决方法：400万条数据的csv，1000万条数据的xml，或者有1亿商品json文件，
        采取的方式：第一时间想到迭代器和生成器
'''
# 递归：把大的事情拆解成小的单元，特点是自己调用自己
# 迭代器和生成器

from xml.etree.ElementTree import iterparse

def parse_and_remove(filname,path):
    # 读取到item的相对路径，使用的是/分割 province/item
    path_parts = path.split('/')
    # 事件  start：某个节点被创建的时产生的开始事件
    #       end：某个节点被创建完成时产生的结束事件
    doc = iterparse(filname,('start','end'))
    # 跳过root元素
    next(doc)
    # 用list模拟一个栈
    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
                # 减少内存消耗的核心语句，把yield产生的元素从它的父节点中删除
                elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass

data = parse_and_remove('./cities.xml', 'province/item')

for item in data:
    print(item.text)


'''
    如果用之前的方法，处理1000000万行的数据，内存占用大概4个G
    如果用parse_and_remove()方法处理，大概占用80M
'''