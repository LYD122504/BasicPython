def match(pattern):
    print('Looking for %s' % pattern)
    while True:
        line =yield
        if pattern in line:
            print(line)
m=match('python')
print(m)
m.send(None)
m.send('hello python')      # 输出: hello python
m.send('java is good')      # 无输出
m.send('I love!')    # 输出: I love python
m.close()
def consumer(func):
    def start(*args,**kwargs):
        cr=func(*args,**kwargs)
        cr.send(None)
        return cr
    return start
@consumer
def match(pattern):
    print('Looking for %s' % pattern)
    while True:
        line =yield
        if pattern in line:
            print(line)
m=match('python')
print(m)
m.send('hello python')      # 输出: hello python
m.send('java is good')      # 无输出
m.send('I love!')    # 输出: I love python
m.close()
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
# follow('../Data/stocklog.csv',printer())
@consumer
def match(pattern, target):
    while True:
        line = yield  # 接收一行
        if pattern in line:
            target.send(line)  # 发送到下一阶段
follow('../Data/stocklog.csv', match('AA', printer()))