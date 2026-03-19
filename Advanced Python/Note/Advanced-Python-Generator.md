---
title: Advanced Python-Generator
date: 2026-03-19 20:27:01
tags:
    - Python
categories: Advanced Python
mathjax: true
---

# Iterators,Generators and Coroutines


<a id="orgdb44a50"></a>

## Iterator

迭代定义经常发生在循环遍历项的时候发生调用,代码如下所示,

```python
a=[2,4,10,37,62]
for x in a:
    print(x)
```

这是一个十分常见的代码编程模式,常见于循环,列表推导式等.他的迭代语法原型为

```python
for x in obj:
    # statements
```

<!--more-->

他的底层语法结构为

```python
_iter=obj.__iter__() # Get iterator object
while True:
    try:
        x=_iter.__next__() # Get next item
    except StopIteration: # No more items
        break
    # statements
```

所有能在for循环中遍历执行的对象,都应该在底层实现迭代协议,如\_\_iter\_\_方法(获取迭代对象),\_\_next\_\_方法(获取迭代的下一个对象).如果迭代器完成迭代,就会返回一个StopIteration.

```python
x=list(range(10))
print(x)
it=x.__iter__()
print(it)
print(it.__next__())
print(it.__next__())
print(it.__next__())
```

自定义容器可以进行委托迭代.这是一种封装模式,如Portfolio类内部有一个列表,其不想暴露列表本身,但仍然想要在外部能够迭代调用.通过迭代委托的方式给内部对象,这样既能够保持了封装性,又可以获得迭代的便利性.

```python
class Portfolio:
    def __init__(self):
        self.holdings=[]
    def __iter__(self):
        return self.holdings.__iter__()
p=Portfolio()
p.holdings.append(1)
p.holdings.append(2)
p.holdings.append(3)
for x in p:
    print(x)
```

生成器则是可以简化自定义迭代的流程,代码如下所示,

```python
class Countdown:
    def __init__(self,n):
        self.n=n
    def __iter__(self):
        n=self.n
        while n>0:
            yield n
            n-=1
c=Countdown(5)
for i in c:
    print(i)
```

这里的yield关键字是生成器的核心,他和普通函数不同,其不会一次性返回所有结果并结束,而是应每次产生一个值并且停止运行.他的方便之处在于不需要手动管理\_\_iter\_\_方法和\_\_next\_\_方法.生成器函数的行为不同还在于他的返回会创建一个生成器对象,但不会开始运行函数,需要注意的是此时是没有产生输出值的.这是因为yield会出现一个惰性行为,计算和迭代推进只在需要的时候才会发生.函数只会在next函数调用的时候执行,yield产生一个值,然后会将函数挂起,函数一直到下一次调用next方法才会恢复执行.生成器具有记忆能力,当他挂起的时候,所有局部变量都会被保存;下次恢复的时候,会从上次停下的地方开始,直到遇见next函数,才会重新停止函数执行.当生成器开始返回值的时候,也就代表迭代的结束.生成器函数实现了与for语句在列表,元组,字典和文件上的使用相同的底层协议.但是我们需要注意的是,生成器函数只能够使用一次,如果我们需要多次使用,应该需要再次定义.

```python
c=Countdown(5)
for i in c:
    print(i)
for i in c:
    print(i)
```

生成器如果耗尽,那么就会抛出StopIteration,无法重置状态.这样可以确保数据流的单向性和内存高效性.因此,引入一个可重复使用的生成器类,只需要在其中创建一个\_\_iter\_\_方法,每次迭代都会重新创建一个新的生成器.

```python
class FRANGE():
    def __init__(self,start,stop,step):
        self.start=start
        self.stop=stop
        self.step=step
    def __iter__(self):
        n=self.start
        while n<self.stop:
            yield n
            n+=self.step
f=FRANGE(0,2,0.35)
for x in f:
    print(x,end=' ')
print()
for x in f:
    print(x,end=' ')
print()
```

并且生成器可以用于转换为列表,元组和实现解包操作.

```python
# s 是一个可重用的生成器类
print(list(s))
print(tuple(s))
name,shares,price=s
```


<a id="orge5180ce"></a>

## Producers & Consumers

生成器常用于生产者-消费者编程相关,其中yield生产值,for消费值.

```python
# producers
import os
import time
def follow(filepath):
    f=open(filepath)
    f.seek(0,os.SEEK_END)
    while True:
        line=f.readline()
        if line=='':
            time.sleep(0.1)
            continue
        yield line
# consumers
for line in follow(filepath):
    print(line)
```

生成器天然适合作为生产者,因为可以按需产生数据,而非一次性将数据存入内存,适合于处理流式数据.利用生成器来构造数据处理管道.其中管道由初始数据生产者,中间数据处理模块和最终数据消费者构成.其结构如下,

![2026-03-09_14-09-05_screenshot](https://github.com/LYD122504/picx-images-hosting/raw/master/20260319/2026-03-09_14-09-05_screenshot.8dxfjdtfoc.png)生产者一般是生成器,当然也可以是列表或者其他的序列容器.yield可以将数据传入给管道.他的作用是负责数据源,不需要知道数据的后续处理方式,只需要负责生成数据.消费者一般是for循环,他会获取数据并且对他们进行操作,消费者是为了驱动整个管道的数据流运行.中间处理模块则是同时消费和生产数据,他会在管道中间修改数据流,并且可以过滤并丢弃数据.当我们用代码完成了管道的架构,此处不会立即运行程序,而只有在消费者开始迭代运行的时候,数据流才会开始流动,而且内存占用仅仅取决于单个阶段处理的数据量.


<a id="org044e1de"></a>

## Coroutine Functions

在生成器中在,yield可以用作表达式.

```python
def match(pattern):
    print('Looking for %s' % pattern)
    while True:
        line =yield
        if pattern in line:
            print(line)
```

这里的yield出现在赋值语句右端的时候,他不再仅仅是产生值,而是等待接受外部发送进来的值,这开启了与程序外双向通信的可能性.上述的yield调用方式,就会形成一个协程函数,它定义了一个外界可以向其发送值的函数,发送的值由yield返回.协程允许数据流入函数内部,这与普通生成器(数据流出)相反,send方法发送的值会成为yield表达式的值并且完成赋值.

```python
m=match('python')
print(m)
m.send(None)
m.send('hello python')      # 输出: hello python
m.send('java is good')      # 无输出
m.send('I love!')    # 输出: I love python
m.close()
```

他的执行方式和生成器一样,调用协程函数也是什么都不会发生,只是返回一个生成器对象.只有在调用在send方法以后才会运行,所以协程函数也是惰性执行.调用函数只会创建对象,必须通过send方法或者next方法对他进行预激活后,再进行后续的函数调用.一般来说协程需要使用send方法来驱动传递数据.

所有协程函数必须首先通过调用send(None)进行预激活,这将会使得执行推进到第一个yield表达式的地方,然后挂起.

```python
m=match('python')
print(m)
m.send(None)
```

我们需要注意的是,我们必须要先完成协程函数的预激活,将程序运行到第一个yield处挂起,然后才可以接受外部发送的数据.这里的send(None)语句就是在完成这一步预激活程序.如果我们不做预激活,而直接使用send(data),那么程序会返回一个TypeError,并告知不可以传入一个非None数据给未激活的生成器.由于这个预激活的操作是对于每个协程函数都需要调用的,因此我们可以使用装饰器来包装协程函数,将预激活操作封装到包装函数中,自动化预激活,这样就可以避免忘记预激活,减少了用户调用协程函数时的样板代码,提高接口的友好性.

```python
def consumer(func):
    def wrapper(*args,**kwargs):
        cr=func(*args,**kwargs)
        cr.send(None)
        return cr
    return wrapper
@consumer
def match(pattern):
    print('Looking for %s' % pattern)
    while True:
        line =yield
        if pattern in line:
            print(line)
```

协程函数和生成器一样也可以用于组成管道.

![2026-03-17_15-30-49_screenshot](https://github.com/LYD122504/picx-images-hosting/raw/master/20260319/2026-03-17_15-30-49_screenshot.1e961hilmh.png)

 我们只需要将协程函数链接在一起,并且通过send()操作将数据推过管道.这与生成器管道(Pull模型,依靠消费者拉取数据)不同,协程函数管道通常是Push模型,由生产者推送数据,数据通过send函数主动推进到下一个阶段,更适合事件驱动的场景.我们给出一些协程管道的代码实例,下面是一个典型的实时监控日志文件的模式

```python
import time
def follow(filename,target):
    f=open(filename)
    f.seek(0,2) #Go to the end of the file
    # 可选，默认值为 0。给offset参数一个定义，表示要从哪个位置开始偏移；0代表从文件开头开始算起，1代表从当前位置开始算起，2代表从文件末尾算起
    while True:
        line=f.readline()
        if line!='':
            target.send(line)
        else:
            time.sleep(0.1)
@consumer
def printer():
    while True:
        line=yield
        print(line)
follow('../Data/stocklog.csv',printer())
```

follow函数在管道中充当了数据源的作用,其不断读取文件新行并且发送给目标,其中的printer是消费者.

在上面的基础上,加上对数据的过滤操作.

```python
@consumer
def match(pattern, target):
    while True:
        line = yield  # 接收一行
        if pattern in line:
            target.send(line)  # 发送到下一阶段
follow('../Data/stocklog.csv', match('AA', printer()))
```

这里形成了一个协作链,match函数接受数据并且过滤后,再发送给printer函数,嵌套调用建立了数据流向.

利用协程函数,我们可以实现对数据的扇出(fan out)

![2026-03-17_16-17-04_screenshot](https://github.com/LYD122504/picx-images-hosting/raw/master/20260319/2026-03-17_16-17-04_screenshot.102qamaare.png)

 协程管道不仅局限于线性链,一个协程可以将数据发送给多个下游协程,当然也可以从多个上游协程处接受数据.


<a id="org5e5db30"></a>

## Ch8\_Ex3 代码解释

这一部分的完整代码如下所示,所调用的包也会同步上传到Github,故我们只专注于讨论这个代码的调用逻辑和结构

```python
from structure import Structure
from cofollow import consumer,follow
from tableformat import create_formatter
import csv
class Ticker(Structure):
    name = String()
    price =Float()
    date = String()
    time = String()
    change = Float()
    open = Float()
    high = Float()
    low = Float()
    volume = Integer()
@consumer
def to_csv(target):
    def producer():
        while True:
            yield line
    reader=csv.reader(producer())
    while True:
        line=yield
        target.send(next(reader))
@consumer
def create_ticker(target):
    while True:
        row = yield
        target.send(Ticker.from_row(row))
@consumer
def negchange(target):
    while True:
        record = yield
        if record.change < 0:
            target.send(record)
@consumer
def ticker(fmt, fields):
    formatter = create_formatter(fmt)
    formatter.headings(fields)
    while True:
        rec = yield
        row = [getattr(rec, name) for name in fields]
        formatter.row(row)
if __name__ == '__main__':
    follow('../Data/stocklog.csv',
           to_csv(
           create_ticker(
           negchange(
           ticker('text', ['name','price','change'])))))
```

首先第一步定义了一个名为Ticker的类,他继承自Structure.他规定了每一条股票数据应有的字段和类型,例如price是浮点数,volume是整数.这为后续对原始字符串的类型转换打下了基础.对于to\_csv函数,他的装饰器的作用是自动执行一次next(coroutine),让协程函数启动并且停止在第一个yields处.这里的producer()是内部生成器,他被定义后不会运行,到后面的reader = csv.reader(producer()),此时producer()被调用返回一个生成器对象,并且csv.reader接受这个生成器作为他的数据源,注意此时producer产生的生成器还是没有执行的,等程序运行到line=yield挂起,直到外界数据源发送数据给line变量,然后producer会将这个line变量传递给csv.reader,然后在通过target.send()将解析好的列表传递给create\_ticker.

create\_ticker协程函数则是一个对象转换协程函数.他的作用是将原始列表按照类定义中的类型信息,把字符串转换为正确的Python类型.negchange函数的作用在这个处理中充当筛选器,如果某行数据不满足条件,就会在这里被丢弃,不会到达最后的打印环节.ticker函数则是数据管道的结束,他不会再往下发送数据,而是一句用户指定的fields提取数据并且格式化输出到控制台.管道的组装顺序,不同于生成器管道的由外层向内层请求数据,协程函数是从后向前定义的,并且是从外层向内层发送数据.


<a id="org2f03c8d"></a>

## Generator Control Flow

生成器支持强制终止和异常处理.close方法表示强制终止生成器,throw方法则是抛出异常.生成器不仅仅是数据流,它还支持控制流.外部代码可以干预生成器的执行,比如强制关闭它(触发清理代码)或在内部抛出异常,这对资源管理非常重要.

调用close方法关闭生成器.

```python
def genfunc():
    try:
        yield item
    except GeneratorExit:  # .close() 被调用
        # 执行清理 (如果有)
        pass
        return
g = genfunc()  # 一个生成器
g.close()
```

如果生成器调用close方法关闭,它相当于会在yield处抛出一个GeneratorExit异常.close方法是确保资源释放的关键,如生成器打开了文件或者网络连接,则可以在调用close方法的时候抛出GeneratorExit异常的时候,在except块中关闭计算机关键资源,防止内存泄露.

使用throw(type[,val[,tb]])方法来抛出异常.

```python
def genfunc():
    try:
        yield item
    except RuntimeError as e:  # 处理异常
        pass
g = genfunc()  # 一个生成器
g.throw(RuntimeError, "You're dead")
```

下我们简单介绍一下throw方法的传入的各个参数.type参数的作用是提供异常类型,其是必选参数,他指定了你想要抛出的异常类别.在执行的时候Python会检查这个类型并且将其抛出.val则表示异常值或异常实例,他是一个可选参数,用于代表异常的具体内容.如果val是一个实例,那么这个实例就是抛出的异常;如果是一个值,那么Python就会调用type(val)来创建一个异常实例;如果省略这个参数,Python则会尝试实例化一个没有参数的type.tb参数则表示回溯对象,这也是一个可选参数,一般来说平时不会调用.traceback对象用于定义异常发生的现场快照(调用栈信息).如果你想要在A处捕获异常,但在B处抛出它,并希望报错信息显示是在A处发生,可以将A处的\_\_traceback\_\_传递给这个参数.

throw()允许外部代码向生成器内部注入异常.这在协程管道中很有用,比如当某个阶段发生错误时,可以向下游传播错误信号,或者通知上游停止生产.需要注意的是异常并不会暂停生成器的存在,而只是允许yield将异常信息抛出.


<a id="org900b3a8"></a>

## Managed Generators

生成器函数并不能单独执行,他必须由其他东西驱动(如for循环或者send方法等).yield语句则表示一个抢占点,生成器会在yield处挂起,直到被外界调用或系统指示才会继续运行.其实这也是协作式多任务的基础,因为生成器需要调度器来分配计算资源,yield则是资源让出控制权的地方,这与操作系统线程的抢占式多任务不同.

我们引入一个manager模块来协调生成器的执行.

![2026-03-17_20-35-36_screenshot](https://github.com/LYD122504/picx-images-hosting/raw/master/20260319/2026-03-17_20-35-36_screenshot.3yf0e4jhn4.png)

 这里的管理器或者调度器就是协作式多任务的核心,他会维护一个生成器队列,轮流调用它们的next方法或者send方法,这使得多个生成器看起来像是在并发运行,实际上是在单线程中交替执行.他的典型应用场景为并发(如tasklets,greenlets等);Actors;事件模拟等.

我们给出如下的示例代码,

```python
def countdown(n):
    while n>0:
        print('T-minus',n)
        yield
        n-=1
def countup(n):
    x=0
    while x<n:
        print('Up we go',x)
        yield
        x+=1
from collections import deque
tasks=deque([countdown(10),countdown(5),countup(20)])
def run():
    while tasks:
        t=tasks.popleft()
        try:
            t.send(None)
            tasks.append(t)
        except StopIteration:
            pass
run()
```

这里的yield没有产生值,也没有接受值,他只不过是自愿让出控制权的信号.任务执行一步,然后暂停让调度器运行其他的任务,这也就是协作式多任务的最简单的形式.他轮询任务队列,每次运行一个任务的一步.如果任务结束的时候就不再放回队列.这种模型非常适合I/O密集型任务,但CPU密集型任务上无法利用多核操作.


<a id="orgbe95cc7"></a>

## 简单异步I/O服务器

```python
from socket import *
from select import select
from collections import deque
```

导入socket模块,用于创建网络套接字.网络套接字也就是socket,是计算机网络中应用程序与网络协议栈之间进行通信的接口.他屏蔽了底层复杂的网络硬件细节,给程序员提供了一个简单的API.一个完整的socket链接由双方的IP,双方的端口以及通信协议(TCP/UDP)唯一确定.select则是操作系统提供的一个系统调用函数,他的核心作用是实现I/O多路复用.简单来说,select能让一个程序同时监视多个网络连接,当其中任何一个连接有数据可读或可写时,通知程序进行处理.导入deque则是创建双端队列,用于高效实现任务队列.

```python
tasks=deque()
recv_wait={} # sock->task
send_wait={} # sock->task
```

tasks用于创建双端队列,用来存放当前可以立即执行的任务.recv\_wait用于记录正在等待接收数据的任务,键是socket对象,值是等待该socket可读的任务;send\_wait用于记录正在等待发送数据的任务,键是socket对象,值是等待该socket可写的任务.这三个容器构建了调度器的任务状态.

```python
def run():
    while any([tasks,recv_wait,send_wait]):
        while not tasks:
            can_recv,can_send,_=select(recv_wait,send_wait,[])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))
        task=tasks.popleft()
        try:
            reason,resource=task.send(None)
            if reason == 'recv':
                recv_wait[resource] = task
            elif reason == 'send':
                send_wait[resource] = task
            else:
                raise RuntimeError('Unknown reason %r' % reason)
        except StopIteration:
            print('Task done')
```

run函数中的while any循环表示是任务队列tasks非空或者还有任务在等待I/O(在recv\_wait和send\_wait),那么循环就继续.while not task循环则是表示如果当前没有可以立即执行的任务,也就是所有任务都在等待I/O;select程序在此阻塞,他会监视recv\_wait中的socket(查看谁有数据可读)和send\_wait中的socket(看谁可以写入数据).can\_recv是select返回的可读socket列表,can\_send是select返回的可写socket列表.for循环的作用则是遍历准备好的可读/可写socket列表,从等待字典中取出对应的任务并从字典中删除,将其引入到可立即执行任务队列,所以如果I/O就绪,唤醒对应任务,让其回到任务队列.task.popleft()则是从任务队列的左端取出一个任务执行.try语法块的task.send(None)则是启动它,使其重新获得CPU资源.后续的任务函数的yield会返回值('recv'和socket)被解包赋值给reason和resource.他会告知调度器暂停的原因为reason,需要关注的资源是resource.按照暂停的原因,将任务挂起在不同的容器中,将控制权重新交还给run循环.当生成器函数执行完毕(没有更多yield且函数返回),会抛出StopIteration异常,打印任务完成,然后run循环继续处理下一个任务.

```python
def tcp_server(address, handler):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        yield 'recv', sock
        client, addr = sock.accept()
        tasks.append(handler(client, addr))
```

socket(AF\_INET, SOCK\_STREAM)的作用是用来制作一个网络通信的工具(套接字对象),其中所用的参数AF\_INET指定使用的是IPv4地址协议,如果使用AF\_INET6则表示支持IPv6地址协议;SOCK\_STREAM指定使用TCP协议,面向连接的,可靠的传输,SOCK\_DREAM表示使用UDP协议.setsockopt(SOL\_SOCKET,SO\_REUSEADDR,1)的作用是允许端口被立即重用.参数的作用是SOL\_SOCKET表示设置的选项层级的Socket层级;SO\_REUSEADDR表示允许地址复用,1表示开启.他的作用是如果关闭服务器程序后,操作系统会让端口进入TIME\_WAIT状态,以确保网络中残留的旧数据包消失.如果没有这一行,立即重启服务器,那么就会报地址占用的错误.bind(address)非套接字分配一个具体的地址,address是一个元组(host,port),如果套接字没有固定的地址,客户端不知道去哪里连接.listen(5)表示将套接字从主动模式切换为被动监听模式,准备接受客户端连接,5表示backlog队列长度,当服务器忙不过来时,操作系统内核可以帮忙暂时排队存放多少个连接请求.如果此时第6个客户端在此时尝试连接,而服务器还没有处理完前5个,第6个连接可能会被直接拒绝.如果不写的话,那么套接字只是一个普通的连接点,无法调用accept()方法来接受新连接.此时sock就会变成一个标准的服务器监听套接字.

while循环是一个死循环,表示服务器程序需要一直运行,不能处理完一个连接就退出,他必须时刻等待新的客户端连接.但是虽然他是一个死循环,但yield的存在是可以主动让出控制权,所以其他任务有机会运行.yield的作用是暂停当前任务,并且向调度器提供自己的I/O兴趣,run函数会将当前的函数放入到recv\_wait字典,键是sock,程序执行权会回到run函数.如果run函数的select发现sock可读,那么重新唤醒tcp\_server任务才会继续向下执行.一般来说accept需要等待连接,但是此时因为select已经可确定了sock上有了链接请求,所以他会马上执行,不需要等待,他返回的client是一个新的socket对象,他不是监听的socket,而是专门用于和这个客户端通信的socket,addr则是客户端的IP地址和端口.append操作则是创建并调度一个新的任务,handler则会根据传入的socket对象和addr地址创建一个任务.上面的并发原理其实是服务器主程序不断等待连接,同时不断创建新的客户任务,处理数据收发.

```python
def echo_handler(client, address):
    print('Connection from', address)
    while True:
        yield 'recv', client
        data = client.recv(1000)
        if not data:
            break
        yield 'send', client
        client.send(b'GOT:' + data)
    print('Connection closed')
```

while True也是一个死循环,因为一个TCP链接建立以后,客户端可能会发送多条消息,而不是只调用一次就会断开,这个循环则确保服务器能持续处理该客户端的多次请求,直到客户端主动断开.yield 'recv',client这个语句会暂停任务,并向外申请可读需求.如果进入了下一步,那么表示client这个socket已经开始接受数据了,recv(1000)的作用则是从socket读取最多1000个字节的数据.需要注意的是实际上recv函数是可能会发生阻塞的,但是我们在此调用的时候已经默认了存在一个socket读取的数据,所以不会阻塞,可以立刻拿到数据.后面的if判断则是判断客户端是否断开连接;data是空字节,表示客户端已经关闭了连接(发送了FIN码),则结束循环;data如果有内容就继续运行.yield 'send',client这个语句会暂停任务,并向外申请可写需求.实际上send也是存在阻塞的可能,操作系统的发送缓冲区会满,这样的话send方法就会发生阻塞,所以需要防止因发送过快导致整个服务器线程卡住.send操作是将收到的数据前面加上GOT,这里需要注意的是网络通信的本质上是二进制,所以计算机网络底层传输的只能是0和1,也就是字节,所以添加的字符串也应该是字节字符串.

完整代码如下

```python
from socket import *
from select import select
from collections import deque
tasks=deque()
recv_wait={} # sock->task
send_wait={} # sock->task
def run():
    while any([tasks,recv_wait,send_wait]):
        while not tasks:
            can_recv,can_send,_=select(recv_wait,send_wait,[])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))
        task=tasks.popleft()
        try:
            reason,resource=task.send(None)
            if reason == 'recv':
                recv_wait[resource] = task
            elif reason == 'send':
                send_wait[resource] = task
            else:
                raise RuntimeError('Unknown reason %r' % reason)
        except StopIteration:
            print('Task done')
def tcp_server(address, handler):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        yield 'recv', sock
        client, addr = sock.accept()
        tasks.append(handler(client, addr))
def echo_handler(client, address):
    print('Connection from', address)
    while True:
        yield 'recv', client
        data = client.recv(1000)
        if not data:
            break
        yield 'send', client
        client.send(b'GOT:' + data)
    print('Connection closed')
if __name__ == '__main__':
    tasks.append(tcp_server(('',25000), echo_handler))
    run()
```

这里的('',25000)中''代表0.0.0.0,意思是监听本机所有网卡(无论是局域网IP,公网IP还是本地回环);25000代表端口号,客户端必须链接这个端口才能找到服务器.


<a id="org4c12825"></a>

## Other Genarator

如果我们考虑如下生成器函数,

```python
def countdown(n):
    while n>0:
        yield n
        n-=1
def countup(n):
    x=0
    while x<n:
        yield x
        x+=1
def up_and_down(n):
    countup(n)
    countdown(n)
```

需要注意的是up\_and\_down函数就算被调用他也不会产生结果,因为他只会获得生成器对象,但不会将其消耗.当然我们可以将函数改写为如下结构,

```python
def up_and_down(n):
    for x in countup(n):
        yield x
    for x in countdown(n):
        yield x
```

我们需要自己驱动生成器,也就是需要使用for循环手动控制每个生成器,但是如果函数结构比较复杂,那么手动管理就会十分复杂,因此我们可以引入yield from语法来将生成器的驱动交给Python解释器驱动,无论什么外部代码运行生成器,都会自行处理,

```python
def up_and_down(n):
    yield from countup(n)
    yield from countdown(n)
```

async的协程我们已在前面提及到了,如感兴趣可以查阅[协程](https://lyd122504.github.io/2025/12/28/Practical-Python-Coroutine/),所以不再赘述.
