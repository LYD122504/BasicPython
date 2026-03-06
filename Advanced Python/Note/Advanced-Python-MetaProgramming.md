---
title: Advanced Python-MetaProgramming
date: 2026-03-06 23:04:46
tags:
    - Python
categories: Advanced Python
mathjax: true
---

# MetaProgramming


<a id="org68f7d6f"></a>

## Decorators

在编写程序中存在大量代码重复的问题,其在编写过程会十分枯燥无聊,并且后续难以维护.元编程涉及编写操作其他代码的代码问题.其相应的应用示例为宏(Marco),包装器(wrapper),切面(aspect).因此其本质上是对代码进行操作.元编程的核心动力是DRY原则(Don't Repeat Yourself). 当发现存在大量代码结构类似的情况,则可以用元编程.与C/C++的宏在编译前处理文本,Python的元编程是在运行的时候操作对象(func,class).其会更加的灵活,更加的动态.装饰器是一个创建另一个函数包装器的函数.包装器则是一个全新的函数,但是他的工作原理和原有函数是完全相同的,接受相同的函数参数可以返回相同的返回值,但是可以增加一些额外的操作.装饰器本质上是接受函数作为参数并返回新函数的高阶函数.理想的装饰器应该是对被装饰器的调用者是透明的,也就是即使换成被装饰了的函数,其调用和返回也不应该导致代码出错.而额外的输出则是由包装器函数实现,但仍然依靠原始函数获得结果

<!--more-->.

```python
def add(x,y):
    return x+y
def logged(func):
    def wrapper(*args,**kwargs):
        print('Calling',func.__name__)
        return func(*args,**kwargs)
    return wrapper
log_add=logged(add)
print(log_add)
print(log_add(3,4))
```

这里我们发现这个logged函数的内部函数wrapper内部调用了func,所以其实wrapper函数就是前面介绍过的闭包函数,这样可以使得wrapper能够记住他要包装的那个专有函数.上面的代码中需要为每个函数编写log\_func=logged(func),这要求我们额外多写很多的重复代码.

```python
@logged
def add(x,y):
    return x+y
# add=logged(add)
```

这相当于是将add的指向函数进行了修改,从原始函数修改到包装器函数.当我们使用装饰器替代函数,会添加一些函数功能,这也就是所谓的装饰.装饰器不修改原函数,而是做一个包装.原函数不变,只是调用路径发生了改变.常用的装饰器如下

```python
@staticmethod
@classmethod
@property
name=decorator(name)
```

装饰器可以在任意时间定义一个涉及函数操作的高阶函数,其主要应用是调试诊断,避免代码重复,启用/禁用可选功能.


<a id="org6bce68a"></a>

## Advanced Decorators

高阶装饰器指的是多重装饰器,装饰器和元数据和带参数的装饰器.装饰器可以多次嵌套使用,

```python
@foo
@bar
@spam
def func():
    pass
# func=foo(bar(spam(func)))
```

执行顺序:装饰器是从下向上的应用;调用顺序:调用函数时,从外向内调用.但是多层嵌套会使得调试更困难,错误堆栈也会更长.但是这个潜逃需要十分注意装饰器的上下顺序,不同的顺序可能会导致结果的不同.当定义一个函数,同时会存储一些额外信息(名称,文档字符串等)

```python
def add(x, y):
    'Adds x and y'
    return x + y
print(add.__name__)
print(add.__doc__)
help(add)
```

内省基础:这些属性(name,doc,module)是工具依赖的基础.装饰器则不会保持这些元数据,因为装饰器实际指向了另一个函数,所以出错的时候函数堆栈跟踪的是包装器函数.

```python
@logged
def add(x, y):
    'Adds x and y'
    return x + y
print(add.__name__)
print(add.__doc__)
```

我们可以手动加上复制函数的元数据的代码.

```python
def logged(func):
    def wrapper(*args,**kwargs):
        print('Calling',func.__name__)
        return func(*args,**kwargs)
    wrapper.__name__=func.__name__
    wrapper.__doc__=func.__doc__
    return wrapper
@logged
def add(x, y):
    'Adds x and y'
    return x + y
print(add.__name__)
print(add.__doc__)
```

当然也可以用如下方式自动的复制函数元数据,

```python
from functools import wraps
def logged(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print('Calling',func.__name__)
        return func(*args,**kwargs)
    return wrapper
@logged
def add(x, y):
    'Adds x and y'
    return x + y
print(add.__name__)
print(add.__doc__)
```

这里会自动将原函数的元数据复制到wrapper函数上去.从上面的代码来看,wraps装饰器是能够接受参数的,所以我们接下来介绍带参数的装饰器.

```python
@decorator(x,y,z)
def func():
    pass
# func=decorator(x,y,z)(func)
```

装饰器函数必须返回一个函数,这个函数会用于创建包装器函数.对于这类带参数的装饰器,实际上有三层的参数嵌套,外层接受装饰器参数,中层接受被装饰函数,内层接受调用参数.其调用链由decorator(x,y,z)返回中层函数,其会被被装饰函数调用.其外部函数用于接受参数,内部函数则是标准的装饰器代码.因此带参数的装饰器更加通用,并且也可以将带参数的装饰器实例化为无参数的装饰器变量.

```python
def logmsg(message):
    def logged(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            print(message.format(name=func.__name__))
            return func(*args,**kwargs)
        return wrapper
    return logged
@logmsg('You called {name}')
def add(x,y):
    return x+y
print(add(3,4))
logged=logmsg('You called {name}')
@logged
def add(x,y):
    return x+y
print(add(3,4))
```


<a id="orgc916e88"></a>

## Class Decorator

装饰器不仅可以应用在函数上,还可以应用在类定义.

```python
@decorator
class Myclass:
    def foo:
        pass
# 上面的相当于Myclass=decorator(Myclass)
```

所以也就是装饰器操作或包装一个类.类装饰器一般常用于自动注册类,验证类结构或者批量修改类方法.大多数类装饰器会检查类定义或做一些特殊处理.类装饰器的语法结构如下所示

```python
def decorator(cls):
    # Do something with cls
    # Return the original class back
    return cls
```

这里我们可以发现类装饰器通常不会修改原始类并且返回.函数装饰器通常会返回一个新的函数,而类装饰器通常直接修改传入的类对象cls并返回相应的类对象.

```python
def logged_getattr(cls):
    # Get the original implementation
    orig_getattribute=cls.__getattribute__
    # Replacement method
    def __getattribute__(self,name):
        print("Getting:",name)
        return orig_getattribute(self,name)
    # Attach to the class
    cls.__getattribute__=__getattribute__
    return cls
@logged_getattr
class MyClass:
    def __init__(self,name,size):
        self.name=name
        self.size=size
    def foo(self):
        pass
s=MyClass(10,9)
print(s.name)
print(s.size)
s.foo()
```

这里我们提供了一个类装饰器的例子,他的作用是在调用类成员的时候,会宣告查看的类成员名称.

现代的Python3.6以上的版本提供了\_\_init\_subclass\_\_方法,他其实比前面介绍的类装饰器更好用,所以我们在此加以解释一下.通常父类不知道子类继承的情况,但是定义了\_\_init\_subclass\_\_的类,是可以在类被继承的时候察觉到子类的存在,并且对子类进行自动化的操作.

```python
class PluginBase:
    subclasses = []
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # 只要有人继承我，我就把它存到列表里，实现自动注册
        cls.subclasses.append(cls)
class VideoPlugin(PluginBase): pass
class AudioPlugin(PluginBase): pass
print(PluginBase.subclasses) 
```

这里的cls表示刚刚创建的子类,这其实也是表示父类可以获取子类的信息.


<a id="orgea4c5b1"></a>

## Type

Python中的任意值都有自己的类型,并且类型其实也是一个可调用对象,我们可以调用他来创建一个同类型的对象.

```python
x=43
print(type(x))
s='Hello'
print(type(s))
items=[1,2,3]
print(type(items))
a=list()
print(a)
b=tuple(items)
print(b)
```

不仅如此,我们自定义创建的类在Python中也是类型的一种.所以类可以自定义一个新类型,他的调用方式和内置类型一样.

```python
class Spam:
    pass
s=Spam()
print(type(s))
print(type(Spam))
```

类是创建的实例的类型,类也是创建实例的可调用对象.我们对于类调用type函数可以得知,类的类型其实是type类.换言之,类其实是type类的一个实例.而type类本身则是由他们自己表示,所以我们定义自己的类其实在Python内部是由type类做的处理,因此我们称type类为元类,简单来说他就是所有类的类.

我们对类的定义过程进行一个解构,首先我们常见的类定义方式如下所示,

```python
class Spam(object):
    def __init__(self,name):
        self.name=name
    def yow(self):
        print("Yow!",self.name)
s=Spam('Test')
s.yow()
```

但实际上我们可以将他分成三步:第一步我们先定义一些需要的函数方法,

```python
def __init__(self,name):
    self.name=name
def yow(self):
    print("Yow!",self.name)
```

第二步我们则是构造方法字典,他的键名是方法名,而他的值则是上面定义的函数对象,两者可以不同,但是不建议,因为会使得程序维护困难,

```python
methods={'__init__':__init__,'yow':yow}
```

最后我们调用type函数来构造一个类

```python
Foo=type('Foo',(object,),methods)
type(clsname,(Base,),methods)
```

这里的第一个参数clsname表示想要创建的类名,第二个参数则表示需要的基类元组,第三个参数则是方法字典.

在此基础上我们给出一个利用type构造函数和命名空间字典来创建类的方式.首先,我们需要准备命名空间,语法如下所示,

```python
__dict__=type.__prepare__('Spam',(object,))
```

在正常的class语句的开始,Python会先调用元类的\_\_prepare\_\_方法,其作用是创建一个用于保存类成员(属性和方法)的字典,他通常返回一个空的dict,但在某些复杂的元类编程中,会返回一个OrderedDict或其他特殊映射.这里传入基类的原因,一是用来检查父类中是否有自定义的元类,如果有,那么Python就会调用其元类的方法而不是type的默认方法,二则是默认情况下会返回一个字典,但是某些高级模块会要求返回有序字典,这样的话,可以保证顺序.

第二步用于填充类信息

```python
__dict__['__qualname__'] = 'Spam'
__dict__['__module__'] = 'modulename'
```

这里其实就是在模拟Python编译器自动完成的工作,\_\_qualname\_\_表示类的限定名,\_\_module\_\_表示类的模块名,如果不手动设置,那么手动创建的类可能会丢失这些元数据.

第三步是执行类体代码也是最为关键的一步

```python
body='''
def __init__(self,name):
    self.name=name
def yow(self):
    print("Yow!",self.name)
'''
exec(body, globals(), __dict__)
```

body表示一个包含函数定义的字符串,exec则是在\_\_dict\_\_这个命名空间里面执行字符串代码.执行后,\_\_dict\_\_中会多出两个键:\_\_init\_\_和yow,它们分别对应定义的函数对象.

第四步,形成真正的类

```python
Spam = type('Spam', (object,), __dict__)
```

整体代码如下

```python
body='''
def __init__(self,name):
    self.name=name
def yow(self):
    print("Yow!",self.name)
'''
__dict__=type.__prepare__('Spam',(object,))
print(__dict__)
__dict__['__qualname__'] = 'Spam'
__dict__['__module__'] = 'modulename'
exec(body,globals(),__dict__)
print(__dict__)
Spam = type('Spam', (object,), __dict__)
```


<a id="org7c3a7c1"></a>

## MetaClass

创建类的类称之为元类,type则是元类的一个实例.Python提供了一个Hook,允许你覆盖类创建步骤.我们在创建类的时候可以选择使用不同于type的元类.使用这个,你可以完全自定义类在创建时发生的事情.其相关的语法调用如下所示,

```python
class Spam(metaclass=type):
    def __init__(self,name):
        self.name=name
    def yow(self):
        print("Yow!",self.name)
s=Spam('Test')
s.yow()
```

我们发现在类创建的时候提供了一个元类参数,其提供一个metaclass关键字参数,在此我们可以设置用于创建类对象的类,也就是所谓的元类选择.只是默认来说我们直接使用type元类,因此我们平时见到的元类并不多,当然我们也可以设置成自己定义的元类.上面提到的用法其实是Python3的语法,在Python2中,我们需要用如下的语法结构,

```python
class Spam:
    __metaclass__=type # Python2 only
    def __init__(self,name):
        self.name=name
    def yow(self):
        print('Yow!',self.name)
```

如果我们不显式的设置元类,那么Python会直接使用父类的元类创建.

```python
class Spam(object):
    def __init__(self,name):
        self.name=name
    def yow(self):
        print('Yow!',self.name)
```

我们提供一种自定义新元类的方式,我们可以通过继承type类并且重定义类的方法,如\_\_new\_\_,\_\_prepare\_\_等等.

```python
class mytype(type):
    @staticmethod
    def __new__(meta,name,bases,methods):
        print('Creating class:',name)
        print('Base classes:',bases)
        print('Methods:',list(methods))
        return super().__new__(meta,name,bases,methods)
```

基于上面定义的元类,我们可以定义一个新的根对象,

```python
class myobject(metaclass=mytype):
    pass
```

为了使用我们上面定义的新元类,我们可以通过继承根类对象来定义自己的类,元类的new方法是用于创建类对象本身,而类的new方法则是创建一个未初始化的类实例对象.

```python
class Spam(myobject):
    def __init__(self, name):
        self.name = name
    def yow(self):
        print("Yow!", self.name)
```


<a id="org6cdbd97"></a>

## Application

元类允许改变类定义过程本身,设置类定义环境,改变实例创建.元类允许监控和操作类定义,他有四个比较关键的拦截点,分别如下所示:

```python
# 在类定义开始之前调用
# 返回一个映射对象,通常是字典或有序字典,这个字典将作为类的命名空间,用于存储类定义过程中产生的属性和方法.
# 允许你控制类属性的存储顺序或收集定义时的元数据
type.__prepare__(name,bases)
# 在类主体代码执行完毕后调用,此时prepare返回的字典已经填满了类属性和方法
# 返回类对象本身
# 真正创建类对象的内存空间,如果返回的不是当前类的实例,那么不会调用元类的__init__
type.__new__(type,name,bases,dict)
# 在实例化类时调用，他是实例创建过程中的第一步
# 返回实例对象
# 分配内存并返回一个未初始化的对象.如果new方法没有返回当前类的实例,那么init方法就不会被调用
cls.__new__(cls,*args,**kwargs)
# 在元类的new方法成功返回类对象后调用,标志类定义完成.
# 必须返回None
# 对创建好的类对象进行额外的配置或修改
type.__init__(cls,name,bases,dict)
# 在类的new方法返回实例对象后调用,此时实例已经存在,但是属性尚未赋值
# 必须返回None
# 初始化实例的属性
cls.__init__(*args,**kwargs)
# 元类方法,所属对象是元类,因为类是元类的实例,因此类可以被调用
# 当你执行Class()实例化对象的时候,会被调用;实际上就是会调用type.__call__
# 返回一个初始化完成的实例对象,他是实例化过程的控制器.默认的call函数内部逻辑是,先调用类的new方法创建实例,再调用类的init初始化实例,并返回实例.重写他可以控制实例化的整个过程.
type.__call__(cls,*args,**kwargs)
```

类定义方法的重复检查

```python
class dupedict(dict):
    def __setitem__(self,key,val):
        assert key not in self, '%s duplicated' % key
        super().__setitem(key,val)
class dupemeta(type):
    def __prepare__(name,bases):
        return dupedict()
class A(metaclass=dupemeta):
    def bar(self):
        pass
    def bar(self):
        pass
```

对类中的每个方法都做装饰器操作,

```python
def decorator(func):
    print('Decorating',func.__name__)
    def wrapper(*args,**kwargs):
        print('Calling',func.__name__)
        return func(*args,**kwargs)
    return wrapper
class meta(type):
    def __new__(cls,name,bases,methods):
        for key,val in methods:
            if callable(val):
                methods[key]=decorator(val)
        return super().__new__(cls,name,bases,methods)
```

实例创建

```python
class meta(type):
    def __call__(cls,*args,**kwargs):
        print('Calling instance of',cls)
        return super().__call__(*args,**kwargs)
class Spam(metaclass=meta):
    def __init__(self, name):
        self.name = name
```

单例模式

```python
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
```
