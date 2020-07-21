'''
    将字典转换成xml(Python数据结构dict，list，object)
'''
from xml.etree.ElementTree import Element

data_dict = {
    'h1': '一级标题',
    'p': '文字段落'
}
root_elem = Element('html')

for key, value in data_dict.items():
    child = Element(key)
    child.text = value
    root_elem.append(child)

print(root_elem)

from xml.etree.ElementTree import tostring

data_str = tostring(root_elem)
print(data_str)

# 给p标签添加width属性，使用set()方法
root_elem.set('width', '200px')
data_str = tostring(root_elem)
print(data_str)

'''
    读取xml文档，修改后将结果写回XML文档
'''
from xml.etree.ElementTree import parse, Element

# 根节点
doc = parse('./myxml.xml')
# 得到根节点名称
root = doc.getroot()
print(root.find('h1'))
root.remove(root.find('h1'))

# 删除 remove(element)   insert(位置，element) 插入
for item in doc.iterfind('units/unit/title'):
    item.text = 'lalalalal'

doc.write('new.xml', xml_declaration=True)