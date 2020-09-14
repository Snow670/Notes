## 一、开启线程的两种方式

在python中开启线程要导入`threading`，它与开启进程所需要导入的模块`multiprocessing`在使用上，有很大的相似性。在接下来的使用中，就可以发现。

同开启进程的两种方式相同：

### 1.1  直接利用利用threading.Thread()类实例化



```python
from threading import Thread
import time
def sayhi(name):
    time.sleep(2)
    print('%s say hello' %name)

if __name__ == '__main__':
    t=Thread(target=sayhi,args=('egon',))
    t.start()
    
    print('主线程')
```

### 1.2 创建一个类，并继承Thread类



```python
from threading import Thread
import time
calss Sayhi(Thread):
    def __init__(self,name):
        super().__init__()
        self.name = name
    def run(self):
        time.sleep(2)
        print("%s say hello" %self.name)

if __name__ == "__main__":
    t = Sayhi("egon")
    t.start()
    print("主线程")
```

### 1.3 在一个进程下开启多个线程与在一个进程下开启多个子进程的区别

#### 1.3.1 谁的开启速度更快？



```python
from threading import Thread
from multiprocessing import Process
import os

def work():
    print('hello')

if __name__ == '__main__':
    #在主进程下开启线程
    t=Thread(target=work)
    t.start()
    print('主线程/主进程')
    '''
    打印结果:
    hello
    主线程/主进程
    '''

    #在主进程下开启子进程
    t=Process(target=work)
    t.start()
    print('主线程/主进程')
    '''
    打印结果:
    主线程/主进程
    hello
    '''
```

> **结论：**由于创建子进程是将主进程完全拷贝一份，而线程不需要，所以线程的创建速度更快。

#### 1.3.2 看看PID的不同



```python
from threading import Thread
from multiprocessing import Process
import os

def work():
    print('hello',os.getpid())

if __name__ == '__main__':
    #part1:在主进程下开启多个线程,每个线程都跟主进程的pid一样
    t1=Thread(target=work)
    t2=Thread(target=work)
    t1.start()
    t2.start()
    print('主线程/主进程pid',os.getpid())

    #part2:开多个进程,每个进程都有不同的pid
    p1=Process(target=work)
    p2=Process(target=work)
    p1.start()
    p2.start()
    print('主线程/主进程pid',os.getpid())


'''
hello 13552
hello 13552
主线程pid: 13552
主线程pid: 13552
hello 1608
hello 6324
'''
```

> **总结：**可以看出，主进程下开启多个线程，每个线程的PID都跟主进程的PID一样；而开多个进程，每个进程都有不同的PID。

#### 1.3.3 练习

**练习一：**利用多线程，实现socket 并发连接
 服务端：



```python
from threading import Thread
from socket import *
import os

tcpsock = socket(AF_INET,SOCK_STREAM)
tcpsock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
tcpsock.bind(("127.0.0.1",60000))
tcpsock.listen(5)

def work(conn,addr):
    while True:
        try:
            data = conn.recv(1024)
            print(os.getpid(),addr,data.decode("utf-8"))
            conn.send(data.upper())
        except Exception:
            break

if __name__ == '__main__':
    while True:
        conn,addr = tcpsock.accept()
        t = Thread(target=work,args=(conn,addr))
        t.start()

"""
开启了4个客户端
服务器端输出：
13800 ('127.0.0.1', 63164) asdf
13800 ('127.0.0.1', 63149) asdf
13800 ('127.0.0.1', 63154) adsf
13800 ('127.0.0.1', 63159) asdf

可以看出每个线程的PID都是一样的。
""
```

客户端：



```python
from socket import *

tcpsock = socket(AF_INET,SOCK_STREAM)
tcpsock.connect(("127.0.0.1",60000))

while True:
    msg = input(">>: ").strip()
    if not msg:continue
    tcpsock.send(msg.encode("utf-8"))
    data = tcpsock.recv(1024)
    print(data.decode("utf-8"))
```

**练习二：**有三个任务，一个接收用户输入，一个将用户输入的内容格式化成大写，一个将格式化后的结果存入文件。



```python
from threading import Thread

recv_l = []
format_l = []

def Recv():
    while True:
        inp = input(">>: ").strip()
        if not inp:continue
        recv_l.append(inp)

def Format():
    while True:
        if recv_l:
            res = recv_l.pop()
            format_l.append(res.upper())

def Save(filename):
    while True:
        if format_l:
            with open(filename,"a",encoding="utf-8") as f:
                res = format_l.pop()
                f.write("%s\n" %res)

if __name__ == '__main__':
    t1 = Thread(target=Recv)
    t2 = Thread(target=Format)
    t3 = Thread(target=Save,args=("db.txt",))
    t1.start()
    t2.start()
    t3.start()
```

#### 1.3.4 线程的join与setDaemon

与进程的方法都是类似的，其实`multiprocessing`模块是模仿`threading`模块的接口；



```python
from threading import Thread
import time
def sayhi(name):
    time.sleep(2)
    print('%s say hello' %name)

if __name__ == '__main__':
    t=Thread(target=sayhi,args=('egon',))
    t.setDaemon(True) #设置为守护线程，主线程结束，子线程也跟着线束。
    t.start()
    t.join()  #主线程等待子线程运行结束
    print('主线程')
    print(t.is_alive())
```

#### 1.3.5 线程相关的其他方法补充

`Thread`实例对象的方法：

- `isAlive()`：返回纯种是否是活跃的；
- `getName()`：返回线程名；
- `setName()`：设置线程名。

`threading`模块提供的一些方法：

- `threading.currentThread()`：返回当前的线程变量
- `threading.enumerate()`：返回一个包含正在运行的线程的列表。正在运行指线程启动后、结束前，不包括启动前和终止后。
- `threading.activeCount()`：返回正在运行的线程数量，与`len(threading.enumerate())`有相同结果。



```python
from threading import Thread
import threading
import os

def work():
    import time
    time.sleep(3)
    print(threading.current_thread().getName())


if __name__ == '__main__':
    #在主进程下开启线程
    t=Thread(target=work)
    t.start()

    print(threading.current_thread().getName()) #获取当前线程名
    print(threading.current_thread()) #主线程
    print(threading.enumerate()) #连同主线程在内有两个运行的线程，返回的是活跃的线程列表
    print(threading.active_count())  #活跃的线程个数
    print('主线程/主进程')

    '''
    打印结果:
    MainThread
    <_MainThread(MainThread, started 140735268892672)>
    [<_MainThread(MainThread, started 140735268892672)>, <Thread(Thread-1, started 123145307557888)>]
    2
    主线程/主进程
    Thread-1
    '''
```

## 二、 Python GIL

**GIL**全称**Global Interpreter Lock**，即全局解释器锁。首先需要明确的一点是GIL并不是Python的特性，它是在实现Python解析器(CPython)时所引入的一个概念。就好比C++是一套语言（语法）标准，但是可以用不同的编译器来编译成可执行代码。有名的编译器例如GCC，INTEL C++，Visual C++等。Python也一样，同样一段代码可以通过CPython，PyPy，Psyco等不同的Python执行环境来执行。像其中的JPython就没有GIL。然而因为CPython是大部分环境下默认的Python执行环境。所以在很多人的概念里CPython就是Python，也就想当然的把GIL归结为Python语言的缺陷。所以这里要先明确一点：GIL并不是Python的特性，Python完全可以不依赖于GIL

### 2.1 什么是全局解释器锁GIL

Python代码的执行由Python 虚拟机(也叫解释器主循环，CPython版本)来控制，Python 在设计之初就考虑到要在解释器的主循环中，同时只有一个线程在执行，即在任意时刻，只有一个线程在解释器中运行。对Python 虚拟机的访问由全局解释器锁（GIL）来控制，正是这个锁能保证同一时刻只有一个线程在运行。
 在多线程环境中，Python 虚拟机按以下方式执行：

1. 设置GIL
2. 切换到一个线程去运行
3. 运行：
    a. 指定数量的字节码指令，或者
    b. 线程主动让出控制（可以调用time.sleep(0)）
4. 把线程设置为睡眠状态
5. 解锁GIL
6. 再次重复以上所有步骤

在调用外部代码（如C/C++扩展函数）的时候，GIL 将会被锁定，直到这个函数结束为止（由于在这期间没有Python 的字节码被运行，所以不会做线程切换）。

### 2.2 全局解释器锁GIL设计理念与限制

GIL的设计简化了CPython的实现，使得对象模型，包括关键的内建类型如字典，都是隐含可以并发访问的。锁住全局解释器使得比较容易的实现对多线程的支持，但也损失了多处理器主机的并行计算能力。
 但是，不论标准的，还是第三方的扩展模块，都被设计成在进行密集计算任务是，释放GIL。
 还有，就是在做I/O操作时，GIL总是会被释放。对所有面向I/O 的(会调用内建的操作系统C 代码的)程序来说，GIL 会在这个I/O 调用之前被释放，以允许其它的线程在这个线程等待I/O 的时候运行。如果是纯计算的程序，没有 I/O 操作，解释器会每隔 100 次操作就释放这把锁，让别的线程有机会执行（这个次数可以通过 sys.setcheckinterval 来调整）如果某线程并未使用很多I/O 操作，它会在自己的时间片内一直占用处理器（和GIL）。也就是说，I/O 密集型的Python 程序比计算密集型的程序更能充分利用多线程环境的好处。

下面是Python 2.7.9手册中对GIL的简单介绍：
 The mechanism used by the CPython interpreter to assure that only one thread executes Python bytecode at a time. This simplifies the CPython implementation by making the object model (including critical built-in types such as dict) implicitly safe against concurrent access. Locking the entire interpreter makes it easier for the interpreter to be multi-threaded, at the expense of much of the parallelism afforded by multi-processor machines.
 However, some extension modules, either standard or third-party, are designed so as to release the GIL when doing computationally-intensive tasks such as compression or hashing. Also, the GIL is always released when doing I/O.
 Past efforts to create a “free-threaded” interpreter (one which locks shared data at a much finer granularity) have not been successful because performance suffered in the common single-processor case. It is believed that overcoming this performance issue would make the implementation much more complicated and therefore costlier to maintain.

> 从上文中可以看到，针对GIL的问题做的很多改进，如使用更细粒度的锁机制，在单处理器环境下反而导致了性能的下降。普遍认为，克服这个性能问题会导致CPython实现更加复杂，因此维护成本更加高昂。

## 三、 Python多进程与多线程对比

有了GIL的存在，同一时刻同一进程中只有一个线程被执行？这里也许人有一个疑问：多进程可以利用多核，但是开销大，而Python多线程开销小，但却无法利用多核的优势？要解决这个问题，我们需要在以下几点上达成共识：

- CPU是用来计算的！
- 多核CPU，意味着可以有多个核并行完成计算，所以多核提升的是计算性能；
- 每个CPU一旦遇到I/O阻塞，仍然需要等待，所以多核对I/O操作没什么用处。

当然，对于一个程序来说，不会是纯计算或者纯I/O，我们只能相对的去看一个程序到底是计算密集型，还是I/O密集型。从而进一步分析Python的多线程有无用武之地。

**分析：**

我们有四个任务需要处理，处理访求肯定是要有并发的效果，解决方案可以是：

- 方案一：开启四个进程；
- 方案二：一个进程下，开启四个进程。

**单核情况下，分析结果：**

- 如果四个任务是计算密集型，没有多核来并行计算，方案一徒增了创建进程的开销，方案二胜；
- 如果四个任务是I/O密集型，方案一创建进程的开销大，且进程的切换速度远不如线程，方案二胜。

**多核情况下，分析结果：**

- 如果四个任务是密集型，多核意味着并行 计算，在python中一个进程中同一时刻只有一个线程执行用不上多核，方案一胜；
- 如果四个任务是I/O密集型，再多的核 也解决不了I/O问题，方案二胜。

> **结论：**现在的计算机基本上都是多核，python对于计算密集型的任务开多线程的效率并不能带来多大性能上的提升，甚至 不如串行（没有大量切换），但是，对于I/O密集型的任务效率还是有显著提升的。

**代码实现对比**

计算密集型：



```python
#计算密集型
from threading import Thread
from multiprocessing import Process
import os
import time
def work():
    res=0
    for i in range(1000000):
        res+=i

if __name__ == '__main__':
    t_l=[]
    start_time=time.time()
    for i in range(100):
        # t=Thread(target=work) #我的机器4核cpu，多线程大概15秒
        t=Process(target=work) #我的机器4核cpu，多进程大概10秒
        t_l.append(t)
        t.start()

    for i in t_l:
        i.join()
    stop_time=time.time()
    print('run time is %s' %(stop_time-start_time))
    print('主线程')
```

I/O密集型：



```python
#I/O密集型
from threading import Thread
from multiprocessing import Process
import time
import os
def work():
    time.sleep(2) #模拟I/O操作，可以打开一个文件来测试I/O,与sleep是一个效果
    print(os.getpid())

if __name__ == '__main__':
    t_l=[]
    start_time=time.time()
    for i in range(500):
        # t=Thread(target=work) #run time is 2.195
        t=Process(target=work) #耗时大概为37秒,创建进程的开销远高于线程，而且对于I/O密集型，多cpu根本不管用
        t_l.append(t)
        t.start()

    for t in t_l:
        t.join()
    stop_time=time.time()
    print('run time is %s' %(stop_time-start_time))
```

> **总结：**
>  应用场景：
>  多线程用于I/O密集型，如socket、爬虫、web
>  多进程用于计算密集型，如金融分析

## 四、锁

### 4.1 同步锁

需求：对一个全局变量，开启100个线程，每个线程都对该全局变量做减1操作；

不加锁，代码如下：



```python
import time
import threading

num = 100  #设定一个共享变量
def addNum():
    global num #在每个线程中都获取这个全局变量
    #num-=1

    temp=num
    time.sleep(0.1)
    num =temp-1  # 对此公共变量进行-1操作

thread_list = []

for i in range(100):
    t = threading.Thread(target=addNum)
    t.start()
    thread_list.append(t)

for t in thread_list: #等待所有线程执行完毕
    t.join()

print('Result: ', num)
```

> **分析：**以上程序开启100线程并不能把全局变量`num`减为0，第一个线程执行`addNum`遇到I/O阻塞后迅速切换到下一个线程执行`addNum`，由于CPU执行切换的速度非常快，在0.1秒内就切换完成了，这就造成了第一个线程在拿到num变量后，在`time.sleep(0.1)`时，其他的线程也都拿到了num变量，所有线程拿到的num值都是100,所以最后减1操作后，就是99。加锁实现。

加锁，代码如下：



```python
import time
import threading

num = 100   #设定一个共享变量
def addNum():
    with lock:
        global num
        temp = num
        time.sleep(0.1)
        num = temp-1    #对此公共变量进行-1操作

thread_list = []

if __name__ == '__main__':
    lock = threading.Lock()   #由于同一个进程内的线程共享此进程的资源，所以不需要给每个线程传这把锁就可以直接用。
    for i in range(100):
        t = threading.Thread(target=addNum)
        t.start()
        thread_list.append(t)

    for t in thread_list:  #等待所有线程执行完毕
        t.join()

    print("result: ",num)
```

> 加锁后，第一个线程拿到锁后开始操作，第二个线程必须等待第一个线程操作完成后将锁释放后，再与其它线程竞争锁，拿到锁的线程才有权操作。这样就保障了数据的安全，但是拖慢了执行速度。
>  **注意：**`with lock`是`lock.acquire()`（加锁）与`lock.release()`（释放锁）的简写。



```python
import threading

R=threading.Lock()

R.acquire()
'''
对公共数据的操作
'''
R.release()
```

#### **GIL** vs **Lock**



```csharp
机智的同学可能会问到这个问题，就是既然你之前说过了，Python已经有一个GIL来保证同一时间只能有一个线程来执行了，为什么这里还需要lock? 
```

首先我们需要达成共识：锁的目的是为了保护共享的数据，同一时间只能有一个线程来修改共享的数据

然后，我们可以得出结论：保护不同的数据就应该加不同的锁。

最后，问题就很明朗了，GIL 与Lock是两把锁，保护的数据不一样，前者是解释器级别的（当然保护的就是解释器级别的数据，比如垃圾回收的数据），后者是保护用户自己开发的应用程序的数据，很明显GIL不负责这件事，只能用户自定义加锁处理，即Lock

**详细的：**

因为Python解释器帮你自动定期进行内存回收，你可以理解为python解释器里有一个独立的线程，每过一段时间它起wake up做一次全局轮询看看哪些内存数据是可以被清空的，此时你自己的程序 里的线程和 py解释器自己的线程是并发运行的，假设你的线程删除了一个变量，py解释器的垃圾回收线程在清空这个变量的过程中的clearing时刻，可能一个其它线程正好又重新给这个还没来及得清空的内存空间赋值了，结果就有可能新赋值的数据被删除了，为了解决类似的问题，python解释器简单粗暴的加了锁，即当一个线程运行时，其它人都不能动，这样就解决了上述的问题，  这可以说是Python早期版本的遗留问题。

### 4.2 死锁与递归锁

所谓死锁：是指两个或两个以上的进程或线程在执行过程中，因争夺资源而造成的一种互相等待的现象，若无外力作用，它们都将无法推进下去。此时称系统处于**死锁状态**，或系统产生了死锁。这此永远在互相等待的进程称**死锁进程**。

如下代码，就会产生死锁：



```python
from threading import Thread,Lock
import time
mutexA=Lock()
mutexB=Lock()

class MyThread(Thread):
    def run(self):
        self.func1()
        self.func2()
    def func1(self):
        mutexA.acquire()
        print('\033[41m%s 拿到A锁\033[0m' %self.name)

        mutexB.acquire()
        print('\033[42m%s 拿到B锁\033[0m' %self.name)
        mutexB.release()

        mutexA.release()

    def func2(self):
        mutexB.acquire()
        print('\033[43m%s 拿到B锁\033[0m' %self.name)
        time.sleep(2)

        mutexA.acquire()
        print('\033[44m%s 拿到A锁\033[0m' %self.name)
        mutexA.release()

        mutexB.release()

if __name__ == '__main__':
    for i in range(10):
        t=MyThread()
        t.start()

'''
Thread-1 拿到A锁
Thread-1 拿到B锁
Thread-1 拿到B锁
Thread-2 拿到A锁
然后就卡住，死锁了
'''
```

**解决死锁的方法**

避免产生死锁的方法就是用**递归锁**，在python中为了支持在同一线程中多次请求同一资源，python提供了可重入锁`RLock`。

这个`RLock`内部维护着一个Lock和一个counter变量，counter记录了`acquire`（获得锁）的次数，从而使得资源可以被多次require。直到一个线程所有的`acquire`都被`release`（释放）后，其他的线程才能获得资源。上面的例子如果使用`RLock`代替`Lock`，就不会发生死锁的现象了。

> `mutexA=mutexB=threading.RLock()` #一个线程拿到锁，counter加1,该线程内又碰到加锁的情况，则counter继续加1，这期间所有其他线程都只能等待，等待该线程释放所有锁，即counter递减到0为止。

### 4.3 信号量Semaphore

同进程的信号量一样。
 用一个粗俗的例子来说，锁相当于独立卫生间，只有一个坑，同一时刻只能有一个人获取锁，进去使用；而信号量相当于公共卫生间，例如有5个坑，同一时刻可以有5个人获取锁，并使用。

`Semaphore`管理一个内置的计数器，每当调用`acquire()`时，内置计数器-1；调用`release()`时，内置计数器+1；计数器不能小于0，当计数器为0时，`acquire()`将阻塞线程，直到其他线程调用`release()`。

**实例：**
 同时只有5个线程可以获得Semaphore，即可以限制最大连接数为5：



```python
import threading
import time

sem = threading.Semaphore(5)
def func():
    if sem.acquire():   #也可以用with进行上下文管理
        print(threading.current_thread().getName()+"get semaphore")
        time.sleep(2)
        sem.release()

for i in range(20):
    t1 = threading.Thread(target=func)
    t1.start()
```

利用`with`进行上下文管理：



```python
import threading
import time

sem = threading.Semaphore(5)

def func():
    with sem:   
        print(threading.current_thread().getName()+"get semaphore")
        time.sleep(2)

for i in range(20):
    t1 = threading.Thread(target=func)
    t1.start()
```

> **注：**信号量与进程池是完全不同一的概念，进程池`Pool(4)`最大只能产生4个进程，而且从头到尾都只是这4个进程，不会产生新的，而信号量是产生一堆线程/进程。

### 4.4 事件Event

同进程的一样

线程的一个关键特性是每个线程都是独立运行且状态不可预测。如果程序中的其他线程通过判断某个线程的状态来确定自己下一步的操作，这时线程同步问题就会变得非常棘手，为了解决这些问题我们使用threading库中的`Event`对象。

`Event`对象包含一个可由线程设置的信号标志，它允许线程等待某些事件的发生。在初始情况下，Event对象中的信号标志被设置为假。如果有线程等待一个Event对象，而这个Event对象的标志为假，那么这个线程将会被 一直阻塞直至该 标志为真。一个线程如果将一个Event对象的信号标志设置为真，它将唤醒所有等待这个Event对象的线程。如果一个线程等待一个已经被 设置 为真的Event对象，那么它将忽略这个事件，继续执行。

Event对象具有一些方法：
 `event = threading.Event()` #产生一个事件对象

- `event.isSet()`：返回event状态值；
- `event.wait()`：如果`event.isSet() == False`，将阻塞线程；
- `event.set()`：设置event的状态值为True，所有阻塞池的线程进入就绪状态，等待操作系统高度；
- `event.clear()`：恢复event的状态值False。

**应用场景：**

例如，我们有多个线程需要连接数据库，我们想要在启动时确保Mysql服务正常，才让那些工作线程去连接Mysql服务器，那么我们就可以采用`threading.Event()`机制来协调各个工作线程的连接操作，主线程中会去尝试连接Mysql服务，如果正常的话，触发事件，各工作线程会尝试连接Mysql服务。



```python
from threading import Thread,Event
import threading
import time,random
def conn_mysql():
    print('\033[42m%s 等待连接mysql。。。\033[0m' %threading.current_thread().getName())
    event.wait()  #默认event状态为False,等待
    print('\033[42mMysql初始化成功，%s开始连接。。。\033[0m' %threading.current_thread().getName())


def check_mysql():
    print('\033[41m正在检查mysql。。。\033[0m')
    time.sleep(random.randint(1,3))
    event.set()   #设置event状态为True
    time.sleep(random.randint(1,3))

if __name__ == '__main__':
    event=Event()
    t1=Thread(target=conn_mysql) #等待连接mysql
    t2=Thread(target=conn_mysql) #等待连接myqsl
    t3=Thread(target=check_mysql) #检查mysql

    t1.start()
    t2.start()
    t3.start()


'''
输出如下：
Thread-1 等待连接mysql。。。
Thread-2 等待连接mysql。。。
正在检查mysql。。。
Mysql初始化成功，Thread-1开始连接。。。
Mysql初始化成功，Thread-2开始连接。。。
'''
```

> **注：**`threading.Event`的`wait`方法还可以接受一个超时参数，默认情况下，如果事件一直没有发生，`wait`方法会一直阻塞下去，而加入这个超时参数之后，如果阻塞时间超过这个参数设定的值之后，`wait`方法会返回。对应于上面的应用场景，如果mysql服务器一直没有启动，我们希望子线程能够打印一些日志来不断提醒我们当前没有一个可以连接的mysql服务，我们就可以设置这个超时参数来达成这样的目的：

上例代码修改后如下：



```python
from threading import Thread,Event
import threading
import time,random
def conn_mysql():
    count = 1
    while not event.is_set():
        print("\033[42m%s 第 <%s> 次尝试连接。。。"%(threading.current_thread().getName(),count))
        event.wait(0.2)
        count+=1
    print("\033[45mMysql初始化成功，%s 开始连接。。。\033[0m"%(threading.current_thread().getName()))

def check_mysql():
    print('\033[41m正在检查mysql。。。\033[0m')
    time.sleep(random.randint(1,3))
    event.set()
    time.sleep(random.randint(1,3))

if __name__ == '__main__':
    event=Event()
    t1=Thread(target=conn_mysql) #等待连接mysql
    t2=Thread(target=conn_mysql) #等待连接mysql
    t3=Thread(target=check_mysql) #检查mysql

    t1.start()
    t2.start()
    t3.start()
```

> 这样，我们就可以在等待Mysql服务启动的同时，看到工作线程里正在等待的情况。应用：连接池。

### 4.5 定时器timer

定时器，指定n秒后执行某操作。



```python
from threading import Timer
 
def hello():
    print("hello, world")
 
t = Timer(1, hello)  #1秒后执行任务hello
t.start()   # after 1 seconds, "hello, world" will be printed
```

### 4.6 线程队列queue

queue队列：使用`import queue`，用法与进程`Queue`一样。

`queue`下有三种队列：

- `queue.Queue(maxsize)` 先进先出，先放进队列的数据，先被取出来；
- `queue.LifoQueue(maxsize)` 后进先出，（Lifo 意为last in first out），后放进队列的数据，先被取出来
- `queue.PriorityQueue(maxsize)` 优先级队列，优先级越高优先取出来。

**举例：**
 先进先出：



```python
import queue

q=queue.Queue()
q.put('first')
q.put('second')
q.put('third')

print(q.get())
print(q.get())
print(q.get())
'''
结果(先进先出):
first
second
third
'''
```

后进先出：



```python
import queue

q=queue.LifoQueue()
q.put('first')
q.put('second')
q.put('third')

print(q.get())
print(q.get())
print(q.get())
'''
结果(后进先出):
third
second
first
'''
```

优先级队列：



```python
import queue

q=queue.PriorityQueue()
#put进入一个元组,元组的第一个元素是优先级(通常是数字,也可以是非数字之间的比较),数字越小优先级越高
q.put((20,'a'))
q.put((10,'b'))
q.put((30,'c'))

print(q.get())
print(q.get())
print(q.get())
'''
结果(数字越小优先级越高,优先级高的优先出队):
(10, 'b')
(20, 'a')
(30, 'c')
'''
```

## 五、协程

协程：是单线程下的并发，又称微线程、纤程，英文名：**Coroutine**。**协程是一种用户态的轻量级线程，协程是由用户程序自己控制调度的。**

**需要强调的是：**

\1. python的线程属于内核级别的，即由操作系统控制调度（如单线程一旦遇到io就被迫交出cpu执行权限，切换其他线程运行）

\2. 单线程内开启协程，一旦遇到io，从应用程序级别（而非操作系统）控制切换

**对比操作系统控制线程的切换，用户在单线程内控制协程的切换，优点如下：**

\1.  协程的切换开销更小，属于程序级别的切换，操作系统完全感知不到，因而更加轻量级

\2. 单线程内就可以实现并发的效果，最大限度地利用cpu。

要实现协程，关键在于用户程序自己控制程序切换，切换之前必须由用户程序自己保存协程上一次调用时的状态，如此，每次重新调用时，能够从上次的位置继续执行

（详细的：协程拥有自己的寄存器上下文和栈。协程调度切换时，将寄存器上下文和栈保存到其他地方，在切回来的时候，恢复先前保存的寄存器上下文和栈）

### 5.1 yield实现协程

我们之前已经学习过一种在单线程下可以保存程序运行状态的方法，即yield，我们来简单复习一下：

- yiled可以保存状态，yield的状态保存与操作系统的保存线程状态很像，但是yield是代码级别控制的，更轻量级
- send可以把一个函数的结果传给另外一个函数，以此实现单线程内程序之间的切换 。



```python
#不用yield：每次函数调用,都需要重复开辟内存空间，即重复创建名称空间,因而开销很大
import time
def consumer(item):
    # print('拿到包子%s' %item)
    x=11111111111
    x1=12111111111
    x3=13111111111
    x4=14111111111
    y=22222222222
    z=33333333333

    pass
def producer(target,seq):
    for item in seq:
        target(item) #每次调用函数,会临时产生名称空间,调用结束则释放,循环100000000次,则重复这么多次的创建和释放,开销非常大

start_time=time.time()
producer(consumer,range(100000000))
stop_time=time.time()
print('run time is:%s' %(stop_time-start_time)) #30.132838010787964


#使用yield：无需重复开辟内存空间，即重复创建名称空间,因而开销小
import time
def init(func):
    def wrapper(*args,**kwargs):
        g=func(*args,**kwargs)
        next(g)
        return g
    return wrapper

init
def consumer():
    x=11111111111
    x1=12111111111
    x3=13111111111
    x4=14111111111
    y=22222222222
    z=33333333333
    while True:
        item=yield
        # print('拿到包子%s' %item)
        pass
def producer(target,seq):
    for item in seq:
        target.send(item) #无需重新创建名称空间,从上一次暂停的位置继续,相比上例,开销小

start_time=time.time()
producer(consumer(),range(100000000))
stop_time=time.time()
print('run time is:%s' %(stop_time-start_time)) #21.882073879241943
```

> **缺点：**
>  协程的本质是单线程下，无法利用多核，可以是一个程序开启多个进程，每个进程内开启多个线程，每个线程内开启协程。
>  协程指的是单个线程，因而一旦协程出现阻塞，将会阻塞整个线程。

**协程的定义（满足1，2，3就可以称为协程）：**

1. 必须在只有一个单线程里实现并发
2. 修改共享数据不需加锁
3. 用户程序里自己保存多个控制流的上下文栈
4. 附加：一个协程遇到IO操作自动切换到其它协程（如何实现检测IO，yield、greenlet都无法实现，就用到了gevent模块（select机制））

> **注意：**yield切换在没有io的情况下或者没有重复开辟内存空间的操作，对效率没有什么提升，甚至更慢，为此，可以用greenlet来为大家演示这种切换。

### 5.2 greenlet实现协程

greenlet是一个用C实现的协程模块，相比与python自带的yield，它可以使你在任意函数之间随意切换，而不需把这个函数先声明为generator。

安装`greenlet`模块
 `pip install greenlet`



```python
from greenlet import greenlet
import time

def t1():
    print("test1,first")
    gr2.switch()
    time.sleep(5)
    print("test1,second")
    gr2.switch()

def t2():
    print("test2,first")
    gr1.switch()
    print("test2,second")

gr1 = greenlet(t1)
gr2 = greenlet(t2)
gr1.switch()


'''
输出结果：
test1,first
test2,first   #等待5秒
test1,second
test2,second
'''
```

可以在第一次switch时传入参数



```python
from greenlet import greenlet
import time
def eat(name):
    print("%s eat food 1"%name)
    gr2.switch(name="alex")
    time.sleep(5)
    print("%s eat food 2"%name)
    gr2.switch()

def play_phone(name):
    print("%s play phone 1"%name)
    gr1.switch()
    print("%s play phone 1" % name)

gr1 = greenlet(eat)
gr2 = greenlet(play_phone)
gr1.switch(name="egon")  #可以在第一次switch时传入参数，以后都不需要
```

> **注意：**`greenlet`只是提供了一种比`generator`更加便捷的切换方式，仍然没有解决遇到I/O自动切换的问题，而单纯的切换，反而会降低程序的执行速度。这就需要用到`gevent`模块了。

### 5.3 gevent实现协程

`gevent`是一个第三方库，可以轻松通过gevent实现并发同步或异步编程，在`gevent`中用到的主要是`Greenlet`,它是以C扩展模块形式接入Python的轻量级协程。`greenlet`全部运行在主程操作系统进程的内部，但它们被协作式地调试。**遇到I/O阻塞时会自动切换任务。**

> **注意：**`gevent`有自己的I/O阻塞，如：`gevent.sleep()和gevent.socket()`；但是`gevent`不能直接识别除自身之外的I/O阻塞，如：`time.sleep(2)`,`socket`等，要想识别这些I/O阻塞，必须打一个补丁：`from gevent import monkey;monkey.patch_all()`。

- 需要先安装`gevent`模块
   `pip install gevent`
- 创建一个协程对象g1
   `g1 =gevent.spawn()`
   `spawn`括号内第一个参数是函数名，如eat，后面可以有多个参数，可以是位置实参或关键字实参，都是传给第一个参数（函数）eat的。



```python
from gevent import monkey;monkey.patch_all()
import gevent

def eat():
    print("点菜。。。")
    gevent.sleep(3)   #等待上菜
    print("吃菜。。。")

def play():
    print("玩手机。。。")
    gevent.sleep(5)  #网卡了
    print("看NBA...")

# gevent.spawn(eat)
# gevent.spawn(play)
# print('主') # 直接结束

#因而也需要join方法,进程或现场的jion方法只能join一个,而gevent的joinall方法可以join多个
g1=gevent.spawn(eat)
g2=gevent.spawn(play)
gevent.joinall([g1,g2])  #传一个gevent对象列表。
print("主线程")

"""
输出结果：
点菜。。。
玩手机。。。    
##等待大概3秒       此行没打印
吃菜。。。
##等待大概2秒          此行没打印
看NBA...
主线程
"""
```

> **注：**上例中的`gevent.sleep(3)`是模拟的I/O阻塞。跟`time.sleep(3)`功能一样。

**同步/异步**



```python
import gevent
def task(pid):
    """
    Some non-deterministic task
    """
    gevent.sleep(0.5)
    print('Task %s done' % pid)

def synchronous():  #同步执行
    for i in range(1, 10):
        task(i)

def asynchronous(): #异步执行
    threads = [gevent.spawn(task, i) for i in range(10)]
    gevent.joinall(threads)

print('Synchronous:')
synchronous()   #执行后，会顺序打印结果

print('Asynchronous:')
asynchronous()  #执行后，会异步同时打印结果，无序的。
```

**爬虫应用**



```python
#协程的爬虫应用

from gevent import monkey;monkey.patch_all()
import gevent
import time
import requests

def get_page(url):
    print("GET: %s"%url)
    res = requests.get(url)
    if res.status_code == 200:
        print("%d bytes received from %s"%(len(res.text),url))

start_time = time.time()
g1 = gevent.spawn(get_page,"https://www.python.org")
g2 = gevent.spawn(get_page,"https://www.yahoo.com")
g3 = gevent.spawn(get_page,"https://www.github.com")
gevent.joinall([g1,g2,g3])
stop_time = time.time()
print("run time is %s"%(stop_time-start_time))
```

上以代码输出结果：



```python
GET: https://www.python.org
GET: https://www.yahoo.com
GET: https://www.github.com
47714 bytes received from https://www.python.org
472773 bytes received from https://www.yahoo.com
98677 bytes received from https://www.github.com
run time is 2.501142978668213
```

**应用：**
 通过gevent实现单线程下的socket并发，**注意：**`from gevent import monkey;monkey.patch_all()`一定要放到导入socket模块之前，否则gevent无法识别socket的阻塞。

服务端代码：



```python
from gevent import monkey;monkey.patch_all()
import gevent
from socket import *

class server:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port


    def conn_cycle(self):   #连接循环
        tcpsock = socket(AF_INET,SOCK_STREAM)
        tcpsock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        tcpsock.bind((self.ip,self.port))
        tcpsock.listen(5)
        while True:
            conn,addr = tcpsock.accept()
            gevent.spawn(self.comm_cycle,conn,addr)

    def comm_cycle(self,conn,addr):   #通信循环
        try:
            while True:
                data = conn.recv(1024)
                if not data:break
                print(addr)
                print(data.decode("utf-8"))
                conn.send(data.upper())
        except Exception as e:
            print(e)
        finally:
            conn.close()

s1 = server("127.0.0.1",60000)
print(s1)
s1.conn_cycle()
```

客户端代码 ：



```python
from socket import *

tcpsock = socket(AF_INET,SOCK_STREAM)
tcpsock.connect(("127.0.0.1",60000))

while True:
    msg = input(">>: ").strip()
    if not msg:continue
    tcpsock.send(msg.encode("utf-8"))
    data = tcpsock.recv(1024)
    print(data.decode("utf-8"))
```

通过gevent实现并发多个socket客户端去连接服务端



```python
from gevent import monkey;monkey.patch_all()
import gevent
from socket import *

def client(server_ip,port):
    try:
        c = socket(AF_INET,SOCK_STREAM)
        c.connect((server_ip,port))
        count = 0
        while True:
            c.send(("say hello %s"%count).encode("utf-8"))
            msg = c.recv(1024)
            print(msg.decode("utf-8"))
            count+=1
    except Exception as e:
        print(e)
    finally:
        c.close()

# g_l = []
# for i in range(500):
#     g = gevent.spawn(client,'127.0.0.1',60000)
#     g_l.append(g)
# gevent.joinall(g_l)

#上面注释代码可简写为下面代码这样。

threads = [gevent.spawn(client,"127.0.0.1",60000) for i in range(500)]
gevent.joinall(threads)
```

## 六、IO多路复用

#### 通过IO多路复用实现同时监听多个端口的服务端

示例一：



```python
# 示例一：
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author : Cai Guangyin

from socket import socket
import select

sock_1 = socket()
sock_1.bind(("127.0.0.1",60000))
sock_1.listen(5)

sock_2 = socket()
sock_2.bind(("127.0.0.1",60001))
sock_2.listen(5)

inputs = [sock_1,sock_2]

while True:
    # IO多路复用
    # -- select方法，内部进行循环操作，哪个socket对象有变化（连接），就赋值给r;监听socket文件句柄有个数限制（1024个）
    # -- poll方法，也是内部进行循环操作，没有监听个数限制
    # -- epoll方法，通过异步回调，哪个socket文件句柄有变化，就会自动告诉epoll，它有变化，然后将它赋值给r;
    # windows下没有epoll方法，只有Unix下有，windows下只有select方法
    r,w,e=select.select(inputs,[],[],0.2)  #0.2是超时时间
        #当有人连接sock_1时，返回的r,就是[sock_1,]；是个列表
        #当有人连接sock_2时，返回的r,就是[sock_2，]；是个列表
        #当有多人同时连接sock_1和sock_2时，返回的r,就是[sock_1,sock_2,]；是个列表
        #0.2是超时时间，如果这段时间内没有连接进来，那么r就等于一个空列表；
    for obj in r:
        if obj in [sock_1,sock_2]:

            conn, addr = obj.accept()
            inputs.append(conn)
            print("新连接来了：",obj)

        else:
            print("有连接用户发送消息来了：",obj)
            data = obj.recv(1024)
            if not data:break
            obj.sendall(data)
```

客户端：



```python
# -*- coding:utf-8 -*-
#!/usr/bin/python
# Author : Cai Guangyin

from socket import *

tcpsock = socket(AF_INET,SOCK_STREAM)   #创建一个tcp套接字
tcpsock.connect(("127.0.0.1",60001))     #根据地址连接服务器

while True:   #客户端通信循环
    msg = input(">>: ").strip()   #输入消息
    if not msg:continue           #判断输入是否为空
        #如果客户端发空，会卡住，加此判断，限制用户不能发空
    if msg == 'exit':break       #退出
    tcpsock.send(msg.encode("utf-8"))   #socket只能发送二进制数据
    data = tcpsock.recv(1024)    #接收消息
    print(data.decode("utf-8"))

tcpsock.close()
```

以上服务端运行时，如果有客户端断开连接则会抛出如下异常：

![img](https:////upload-images.jianshu.io/upload_images/5431215-5dd4c555061641f4.png?imageMogr2/auto-orient/strip|imageView2/2/w/668/format/webp)

异常

#### 改进版如下

收集异常并将接收数据和发送数据分开处理
 示例二：



```python
# 示例二
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author : Cai Guangyin

from socket import *
import select

sk1 = socket(AF_INET,SOCK_STREAM)
sk1.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
sk1.bind(("127.0.0.1",60000))
sk1.listen(5)

sk2 = socket(AF_INET,SOCK_STREAM)
sk2.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
sk2.bind(("127.0.0.1",60001))
sk2.listen(5)


inputs = [sk1,sk2]
w_inputs = []

while True:
    r,w,e = select.select(inputs,w_inputs,inputs,0.1)
    for obj in r:
        if obj in [sk1,sk2]:
            print("新连接：",obj.getsockname())
            conn,addr = obj.accept()
            inputs.append(conn)

        else:
            try:
                # 如果客户端断开连接，将获取异常，并将收取数据data置为空
                data = obj.recv(1024).decode('utf-8')
                print(data)
            except Exception as e:
                data = ""

            if data:
                # 如果obj能正常接收数据，则认为它是一个可写的对象，然后将它加入w_inputs列表
                w_inputs.append(obj)
            else:
                # 如果数据data为空，则从inputs列表中移除此连接对象obj
                print("空消息")
                obj.close()
                inputs.remove(obj)


        print("分割线".center(60,"-"))

    # 遍历可写的对象列表，
    for obj in w:
        obj.send(b'ok')
        # 发送数据后删除w_inputs中的此obj对象，否则客户端断开连接时，会抛出”ConnectionResetError“异常
        w_inputs.remove(obj)
```

## 七、socketserver实现并发

基于TCP的套接字，关键就是两个循环，一个连接循环，一个通信循环。

SocketServer内部使用 IO多路复用 以及 “多线程” 和 “多进程” ，从而实现并发处理多个客户端请求的Socket服务端。即：每个客户端请求连接到服务器时，Socket服务端都会在服务器是创建一个“线程”或者“进程” 专门负责处理当前客户端的所有请求。

`socketserver`模块中的类分为两大类：server类（解决链接问题）和request类（解决通信问题）

server类：

![img](https:////upload-images.jianshu.io/upload_images/5431215-579078e965b1f872.png?imageMogr2/auto-orient/strip|imageView2/2/w/451/format/webp)

server类

request类：

![img](https:////upload-images.jianshu.io/upload_images/5431215-932b407b69d66ae2.png?imageMogr2/auto-orient/strip|imageView2/2/w/335/format/webp)

request类

线程server类的继承关系：

![img](https:////upload-images.jianshu.io/upload_images/5431215-aa86320d1511f1c7.png?imageMogr2/auto-orient/strip|imageView2/2/w/816/format/webp)

线程server类的继承关系

进程server类的继承关系：

![img](https:////upload-images.jianshu.io/upload_images/5431215-81d8e01a32108bf6.png?imageMogr2/auto-orient/strip|imageView2/2/w/791/format/webp)

进程server类的继承关系

request类的继承关系：

![img](https:////upload-images.jianshu.io/upload_images/5431215-69eb36986bfcfa1c.png?imageMogr2/auto-orient/strip|imageView2/2/w/392/format/webp)

request类的继承关系

以下述代码为例，分析socketserver源码：



```python
ftpserver=socketserver.ThreadingTCPServer(('127.0.0.1',8080),FtpServer)
ftpserver.serve_forever()
```

查找属性的顺序：`ThreadingTCPServer` --> `ThreadingMixIn` --> `TCPServer->BaseServer`

1. 实例化得到ftpserver，先找类`ThreadingTCPServer`的`__init__`,在`TCPServer`中找到，进而执行`server_bind,server_active`
2. 找`ftpserver`下的`serve_forever`,在`BaseServer`中找到，进而执行`self._handle_request_noblock()`，该方法同样是在`BaseServer`中
3. 执行`self._handle_request_noblock()`进而执行`request, client_address = self.get_request()`（就是`TCPServer`中的`self.socket.accept()`），然后执行`self.process_request(request, client_address`)
4. 在`ThreadingMixIn`中找到`process_request`，开启多线程应对并发，进而执行`process_request_thread`，执行`self.finish_request(request, client_address)`
5. 上述四部分完成了链接循环，本部分开始进入处理通讯部分，在`BaseServer`中找到`finish_request`,触发我们自己定义的类的实例化，去找`__init__`方法，而我们自己定义的类没有该方法，则去它的父类也就是`BaseRequestHandler`中找....

> **源码分析总结：**
>  基于tcp的socketserver我们自己定义的类中的

- `self.server`  即套接字对象
- `self.request`  即一个链接
- `self.client_address`  即客户端地址

> 基于udp的socketserver我们自己定义的类中的

- `self.request`是一个元组（第一个元素是客户端发来的数据，第二部分是服务端的udp套接字对象），如`(b'adsf', <socket.socket fd=200, family=AddressFamily.AF_INET, type=SocketKind.SOCK_DGRAM, proto=0, laddr=('127.0.0.1', 8080)>)`
- `self.client_address`即客户端地址。

### 6.1 `ThreadingTCPServer`

ThreadingTCPServer实现的Soket服务器内部会为每个client创建一个 “线程”，该线程用来和客户端进行交互。

使用ThreadingTCPServer:

- 创建一个继承自 SocketServer.BaseRequestHandler 的类
- 类中必须定义一个名称为 handle 的方法
- 启动ThreadingTCPServer。
- 启动serve_forever() 链接循环

服务端：



```python
import socketserver

class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        # print(addr)
        conn.sendall("欢迎致电10086，请输入1XXX，0转人工服务。".encode("utf-8"))
        Flag = True
        while Flag:
            data = conn.recv(1024).decode("utf-8")
            if data == "exit":
                Flag = False
            elif data == '0':
                conn.sendall("您的通话可能会被录音。。。".encode("utf-8"))
            else:
                conn.sendall("请重新输入。".encode('utf-8'))

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(("127.0.0.1",60000),MyServer)
    server.serve_forever()  #内部实现while循环监听是否有客户端请求到达。
```

客户端：



```python
import socket

ip_port = ('127.0.0.1',60000)
sk = socket.socket()
sk.connect(ip_port)
sk.settimeout(5)

while True:
    data = sk.recv(1024).decode("utf-8")
    print('receive:',data)
    inp = input('please input:')
    sk.sendall(inp.encode('utf-8'))
    if inp == 'exit':
        break
sk.close()
```

## 七、基于UDP的套接字

- `recvfrom(buffersize[, flags])`接收消息，buffersize是一次接收多少个字节的数据。
- `sendto(data[, flags], address)` 发送消息，data是要发送的二进制数据，address是要发送的地址，元组形式，包含IP和端口

服务端：



```python
from socket import *
s=socket(AF_INET,SOCK_DGRAM)  #创建一个基于UDP的服务端套接字，注意使用SOCK_DGRAM类型
s.bind(('127.0.0.1',8080))  #绑定地址和端口，元组形式

while True:    #通信循环
    client_msg,client_addr=s.recvfrom(1024) #接收消息
    print(client_msg)
    s.sendto(client_msg.upper(),client_addr) #发送消息
```

客户端：



```python
from socket import *
c=socket(AF_INET,SOCK_DGRAM)   #创建客户端套接字

while True:
    msg=input('>>: ').strip()
    c.sendto(msg.encode('utf-8'),('127.0.0.1',8080)) #发送消息
    server_msg,server_addr=c.recvfrom(1024) #接收消息
    print('from server:%s msg:%s' %(server_addr,server_msg))
```

**模拟即时聊天**
 由于UDP无连接，所以可以同时多个客户端去跟服务端通信

服务端：



```python
from socket import *

server_address = ("127.0.0.1",60000)
udp_server_sock = socket(AF_INET,SOCK_DGRAM)
udp_server_sock.bind(server_address)

while True:
    qq_msg,addr = udp_server_sock.recvfrom(1024)
    print("来自[%s:%s]的一条消息：\033[32m%s\033[0m"%(addr[0],addr[1],qq_msg.decode("utf-8")))
    back_msg = input("回复消息：").strip()
    udp_server_sock.sendto(back_msg.encode("utf-8"),addr)

udp_server_sock.close()
```

客户端：



```python
from socket import *

BUFSIZE = 1024
udp_client_sock = socket(AF_INET,SOCK_DGRAM)
qq_name_dic = {
    "alex":("127.0.0.1",60000),
    "egon":("127.0.0.1",60000),
    "seven":("127.0.0.1",60000),
    "yuan":("127.0.0.1",60000),
}

while True:
    qq_name = input("请选择聊天对象：").strip()
    while True:
        msg = input("请输入消息，回车发送：").strip()
        if msg == "quit":break
        if not msg or not qq_name or qq_name not in qq_name_dic:continue
        print(msg,qq_name_dic[qq_name])
        udp_client_sock.sendto(msg.encode("utf-8"),qq_name_dic[qq_name])

        back_msg,addr = udp_client_sock.recvfrom(BUFSIZE)
        print("来自[%s:%s]的一条消息：\033[32m%s\033[0m" %(addr[0],addr[1],back_msg.decode("utf-8")))
udp_client_sock.close()
```

> **注意：**
>  1.你单独运行上面的udp的客户端，你发现并不会报错，相反tcp却会报错，因为udp协议只负责把包发出去，对方收不收，我根本不管，而tcp是基于链接的，必须有一个服务端先运行着，客户端去跟服务端建立链接然后依托于链接才能传递消息，任何一方试图把链接摧毁都会导致对方程序的崩溃。

> 2.上面的udp程序，你注释任何一条客户端的sendinto，服务端都会卡住，为什么？因为服务端有几个recvfrom就要对应几个sendinto，哪怕是sendinto(b'')那也要有。

> 3.`recvfrom(buffersize)`如果设置每次接收数据的字节数，小于对方发送的数据字节数，如果运行Linux环境下，则只会接收到`recvfrom()`所设置的字节数的数据；而如果运行windows环境下，则会报错。

**基于socketserver**实现多线程的UDP服务端：



```python
import socketserver

class MyUDPhandler(socketserver.BaseRequestHandler):
    def handle(self):
        client_msg,s=self.request
        s.sendto(client_msg.upper(),self.client_address)

if __name__ == '__main__':
    s=socketserver.ThreadingUDPServer(('127.0.0.1',60000),MyUDPhandler)
    s.serve_forever()
```