a=[2,4,10,37,62]
# Iterate over a
for x in a:
    print(x)
# 底层实现
_iter=a.__iter__()
while True:
    try:
        x=_iter.__next__()
    except StopIteration:
        break
    print(x)
x=list(range(10))
print(x)
it=x.__iter__()
print(it)
print(it.__next__())
print(it.__next__())
print(it.__next__())
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

def countdown(n):
    print('Counting down from',n)
    while n>0:
        yield n
        n-=1
for i in countdown(10):
    print('T-minus',i)
x=countdown(10)
print(next(x))

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
for i in c:
    print(i)

# A Simple Generator
def frange(start,stop,step):
    while start<stop:
        yield start
        start+=step
f=frange(0,2,0.25)
for x in f:
    print(x,end=' ')
print()
for x in f:
    print(x,end=' ')
print()
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
# Adding Iteration to Objects
from stock import Stock
s=Stock('GOOG',100,490.1)
for val in s:
    print(val)
# The Surprising Power of Iteration
print(list(s))
print(tuple(s))
name,shares,price=s
print(name)
print(shares)
print(price)
a=Stock('GOOG',100,490.1)
print(a==s)
# Monitoring a streaming data source
from follow import follow
for line in follow('../Data/stocklog.csv'):
    row = line.split(',')
    name = row[0].strip('"')
    price = float(row[1])
    change = float(row[4])
    if change < 0:
        print('%10s %10.2f %10.2f' % (name, price, change))