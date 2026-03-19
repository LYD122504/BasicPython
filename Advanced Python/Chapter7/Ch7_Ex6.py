class dupedict(dict):
    def __setitem__(self,key,value):
        assert key not in self, '%s duplicated' % key
        super().__setitem__(key,value)
class dupemeta(type):
    @classmethod
    def __prepare__(cls,name,bases):
        return dupedict()
class A(metaclass=dupemeta):
    def bar(self):
        pass
    def foo(self):
        pass

def decorator(func):
    print('Decorating',func.__name__)
    def wrapper(*args,**kwargs):
        print('Calling',func.__name__)
        return func(*args,**kwargs)
    return wrapper
class meta(type):
    def __new__(meta,name,bases,methods):
        for key,val in methods.items():
            if callable(val):
                methods[key]=decorator(val)
        return super().__new__(meta,name,bases,methods)
class Spam(metaclass=meta):
    def bar(self):
        pass
    def foo(self):
        pass
s=Spam()
s.bar()

class meta(type):
    def __call__(cls,*args,**kwargs):
        print('Calling instance of',cls)
        return super().__call__(*args,**kwargs)
class Spam(metaclass=meta):
    def __init__(self, name):
        self.name = name

s = Spam('Guido')
print(s)

from validate import Validator
print(Validator.validators)
import stock
s=stock.Stock('GOOG',100,490.1)
print(s)
from reader import read_csv_as_instances
portfolio=read_csv_as_instances('../Data/portfolio.csv',stock.Stock)
print(portfolio)
from tableformat import create_formatter,print_table
formatter=create_formatter('text')
print_table(portfolio,['name','shares','price'],formatter)

class meta(type):
    _instance=None
    def __call__(cls,*args,**kwargs):
        if not cls._instance:
            cls._instance=super().__call__(*args,**kwargs)
        return cls._instance
class Spam(metaclass=meta):
    def __init__(self,name):
        print('Creating Spam')
        self.name=name
s=Spam('Test')
s1=Spam('Test1')
print(s1.name)
print(id(s)==id(s1))