def countdown(n):
    while n>0:
        yield n
        n-=1
def countup(end):
    n = 0
    while n < end:
        yield n
        n += 1
def up_and_down(n):
    for x in countup(n):
        yield x
    for x in countdown(n):
        yield x
for x in up_and_down(10):
    print(x)
def up_and_down(n):
    yield from countup(n)
    yield from countdown(n)
for x in up_and_down(5):
    print(x)
from cofollow import consumer,receive
@consumer
def printer():
    while True:
        item=yield
        print('Got:',item)
p=printer()
p.send('Hello')
p.send('World!')
@consumer
def print_int():
    while True:
        item=yield from receive(int)
        print('Got:',item)
p=print_int()
p.send(42)