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
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 25000))

while True:
    msg = input("输入消息: ")
    if not msg: break
    s.send(msg.encode())
    print("收到回复:", s.recv(1024).decode())

s.close()