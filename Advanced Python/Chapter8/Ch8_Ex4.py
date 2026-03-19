'''
from follow import follow
f= follow('../Data/stocklog.csv')
print(next(f))
del f
f = follow('../Data/stocklog.csv')
for line in f:
    print(line,end='')
    if 'IBM' in line:
        f.close()
for line in f:
    print(line, end='')
f = follow('../Data/stocklog.csv')
for line in f:
    print(line,end='')
    if 'IBM' in line:
        break
for line in f:
    print(line,end='')
    if 'IBM' in line:
        break
f.close()
'''
from cofollow import printer
p=printer()
p.send('hello')
p.send(42)
p.throw(ValueError('It failed'))
try:
    int('n/a')
except ValueError as e:
    p.throw(e)