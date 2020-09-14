'''
from multiprocessing import Process,Queue

q = Queue(3)
q.put(1)
q.put(2)
q.put(3)
#block 为True, timeout=3 表示该方法会阻塞3s
q.put(4,timeout=3)
#超出队列中的数据限制，会立刻报错queue.Full
q.put(5,block=False)
'''

#队列取出
'''
from multiprocessing import Process,Queue
 
q = Queue(3)
q.put(1)
q.put(2)
q.put(3)
print(q.full())
print(q.get())
print(q.get())
print(q.get())
print(q.empty())
'''

#生产者和消费者
'''
from multiprocessing import Process,Queue
import time,random

def consumer(q,name):
    while True:
        time.sleep(random.randint(1,3))
        res = q.get()
        print('消费者%s拿到了包子'%name)

def producer(seq,q):
    for i in seq:
        time.sleep(random.randint(1,3))
        print('生产者%s生产了包子'%i)
        q.put(i)

if __name__ == '__main__':
    q = Queue()
    consumer_l = ['scz%s'%i for i in range(5)]
    baozi_l = ['包子%s'%i for i in range(5)]
    for i in consumer_l:
        c = Process(target=consumer,args=(q,i,))
        c.start()
    print(baozi_l,q)

'''
#进程池
from multiprocessing import Pool
import time

def work(n):
    pritn('开工了。。。')
    time.sleep(3)
    return n**2

if __name__ == "__main__":
    q = Pool()
    res = q.apply_async(work,args=(2,))
    q.close()
    q.join()
    print(res.get())



