''''
from  multiprocessing import Process

import time
import random 

def sing(name):
    print("是%s在singing"%name)
    time.sleep(random.randint(1,3))
    print('%s唱完了'%name)


if __name__ == '__main__':
    p1 = Process(target=sing,args=('aa',))
    p2 = Process(target=sing,args=('bb',))
    p3 = Process(target=sing,args=('cc',))

    p1.start()
    p2.start()
    p3.start()

    print('主进程')
'''

#———————————第二种创建进程——————————————————————
#创建一个类，然后集成Process类，但是必须定义一个run()方法


'''
import multiprocessing import process
import time
import random

class Sing(Process):
    def __init__(self,name):
        super(Sing,self).__init__()
        self.name = name
    def run(self):
        print('%s在唱歌'%self.name)
        time.sleep(random.randint(1,3))
        print('%s唱完了'%self.name)

if __name__ == '__main__':
    p1 = Sing('aa')
    p2 = Sing('bb')
    p3 = Sing('cc')

    p1.start()
    p2.start()
    p3.start()

'''

#-----------Process方法----------
'''
from multiprocessing import Process
import time
import random

def sing(name):
    print("是%s在singing"%name)
    time.sleep(random.randint(1,3))
    print('%s唱完了'%name)


if __name__ == '__main__':
    p1 = Process(target=sing,args=('aa',))
    p2 = Process(target=sing,args=('bb',))
    p3 = Process(target=sing,args=('cc',))

    #设置p2为守护进程
    p2.daemon = True
    p1.start()
    p2.start()
    #关闭p1
    p1.terminate()
    print('p1 is alive',p1.is_alive())
    p3.start()
    print(p3.pid)
    p3.join(2)
    print('主进程') 
'''

#-----for循环--------

from multiprocessing import Process
import time 
import random

def sing(name):
    print("是%s在singing"%name)
    time.sleep(random.randint(1,3))
    print('%s唱完了'%name)


if __name__ == '__main__':
    name_list = ['aa','bb','cc']
    process_list = []
    for name in name_list:
        p = Process(target=sing,args=(name,))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()
    print('主进程')



