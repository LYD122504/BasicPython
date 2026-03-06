---
title: Advanced Python-Working with Code
date: 2026-02-27 09:30:52
tags:
    - Python
categories: Advanced Python
mathjax: true
---

# Working with Code


<a id="orge8c233a"></a>

## Variable Arguments

函数参数表示函数可以操作传入的参数,其中的基本传入方式有如下两种:

```python
func(1,2,3) # 位置参数
func(x=1,y=2,z=3) # 关键字参数
```

我们可以混合使用这两种参数传入风格,但是位置参数必须始终在关键字参数前面传入,而且需要遵守每个参数都必须有且仅有一个值,如

```python
def fun(x,*args):
    pass
func(1,x=1) # 这会报错
```

混合使用参数风格增加了调用的灵活性,尤其是当函数参数比较多的时候,关键字参数能够提高代码的可读性.

<!--more-->

可变数目参数则是指可以接受任意数目的位置参数或关键字参数.先介绍可变位置参数,代码结构如下,

```python
def func(x,*args):
    print(x)
    print(args)
```

其表示至少需要一个参数传入给x,而其余参数则会以元组的方式传入给args.同样可以接受相应的关键字参数,代码结构如下

```python
def foo(x,y,**kwargs):
    print(x)
    print(y)
    print(kwargs)
foo(2,3,flag=True,mode='fast',header="debug")
```

其余的关键字参数则会以字典的形式传入给kwargs.二者还可以合并使用,如

```python
def func(*args,**kwargs):
    pass
```

这表示这个函数接受任意数目的位置参数或关键字参数,唯一需要注意的是,位置参数必须在关键字参数前出现.这个的用处一般是用于编写包装器或者将函数的参数转移给另一个函数.\*args和\*\*kwargs是编写装饰器的关键,因为它允许包装函数接受被包装函数所能接受的所有参数,而不需要知道他的具体参数签名.这里的args和kwargs只是一个约定俗成的名字,可以根据自己喜好更换,但不是很建议.

我们前面提到可变位置参数传入函数内会以元组的形式存储,可变关键字参数则是以字典的形式存储,所以其实元组和字典也是可以通过解包的方式以各个独立参数的形式传入函数的.元组是通过\*做解包,而字典则是通过\*\*做解包.这其实就是可变参数的逆过程,我们在定义函数的时候用\*来收集函数参数,而在调用时则用\*对元组进行解包.这一操作一般用在配置管理,将配置项提前存储在字典,然后调用函数一次性解包传入,使得代码更加整洁.


<a id="org45e9817"></a>

## Scoping Rules

程序将值赋给变量的时候,一般是在两个大作用域下完成的,全局作用域和局部作用域.

```python
x=value # Global variable
def func:
    y=value # Local variable
```

所以简单来看全局作用域就是在函数外赋值,局部作用域则是在函数内赋值.基本上所有的语句都在这两个作用域中执行.全局作用域始终是定义函数的模块,局部作用域则函数私有的,或者与全局作用域的相同字典.变量的查找顺序是遵循LEGB.需要注意的是,Python中其实没有真正的全局变量只有模块级变量,因为每个python文件都是一个模块,具有自己的全局命名空间.

如果我们希望在函数中修改全局变量,如果只是用普通的x=val,那么会创建一个同名的局部变量,从而覆盖了全局变量的读取.如果需要修改全局变量,我们需要使用global声明,并且需要在使用前调用,而且仅对于要被修改的全局变量是必须的,因为全局变量已经可读.

```python
x=1
def func():
    global x
    x=2
```

在函数中可以直接读取全局变量,而不用global声明,只有我们希望修改全局变量,才应该对其做global声明.但是如果全局变量是可变的,例如x=[],如果我们只是做append之类的原地操作,那么是不需要做global声明的.因为x指向的是列表对象,原地操作则是不会修改变量的指向,我们只是填充列表对象,因此不需要做声明,只有在重新绑定才会需要声明global声明.我们需要注意的是尽量不要在函数内部修改全局变量的状态.

globals()函数可以以字典形式返回全局作用域的内容;locals()函数可以以字典形式返回局部作用域的内容.可以借助这两个函数检查代码实现.需要注意的是locals和globals函数在模块中调用,那么他们的输出会是一样的.

```python
x=1
def func():
    test=1
    print(globals())
    print(locals())
print(globals())
print(locals())
```

内置函数会存在在builtins module.如果查找不到相应的变量,则是会去builtins module中查找.并不建议修改builtins modules.

我们给出一个比较技巧性的Python编程技巧,

```python
class Stock(Structure):
    _fields=('name','shares','price')
    @staticmethod
    def _init():
        locs=sys._getframe(1).f_locals # Get callers local variables
        self = locs['self']
        for name, val in locs.items():
            if name == 'self': continue
            setattr(self, name, val)
    def __init__(self,name,shares,price):
        self._init()
```

我们主要介绍其中的sys.\_getframe(1).f\_locals的作用.sys.\_getframe(n)是一个用于内省的函数,用于访问当前的调用栈.n=0代表当前函数,也就是\_init方法本身;n=1代表调用当前函数的那个函数,也就是\_\_init\_\_方法,所以此时获取的是\_\_init\_\_执行的时候的栈帧对象.f\_locals则是栈帧对象的一个属性,返回一个字典,包含了该函数作用域的所有局部变量,上面的调用则是大体上可能会返回如下结果,

```python
{
    'self': <Stock 对象实例>,
    'name': 'ACME',
    'shares': 50,
    'price': 91.1
}
```

所以locs的赋值过程相当于就像是\_init方法读取了\_\_init\_\_方法的内部所有变量.


<a id="org17ce4ab"></a>

## Function objects

当我们完成了函数的定义的时候,函数其实会变成一个可以操作的对象,他可以用于变量赋值,存取容器以及传入参数.函数的第一行可以是字符串,并且会被默认为文档字符串,其会存储在函数的\_\_doc\_\_属性.help函数可以查看函数的文档字符串,建议用三引号编写多行文档字符串.

```python
def func(a, b):
    'This function does something.'
    pass
print(func.__doc__)
help(func)
```

在函数定义的时候,可以添加一些注释.参数和返回值是允许被添加注释的,如

```python
def func(a:int,b:int)->int:
    pass
```

我们可以在函数的\_\_annotations\_\_属性中查看相应的注释.但这类注释什么都不会做,他只是提供变量期待的类型信息,不会强制要求满足类型.我们可以给函数添加任意形式的属性,他会存放在函数的\_\_dict\_\_属性中,这可以使函数具有静态变量的状态.这一特性一般用于给函数标记属性,例如在Web开发的时候用来标注某个函数需要认证,则可使用如下的代码.

```python
func.requires_auth=t=True
```

我们可以检查函数的几乎所有属性.我们罗列如下

```python
print(func.__name__)
```

用于获取函数的名称,以字符串形式返回

```python
def func(a,b=1):
    pass
print(func.__defaults__)
```

获取函数位置参数的默认值,以元组的形式返回,如果没有,那就返回None.

```python
def func(a,*,b=1):
    pass
print(func.__defaults__)
```

获取函数中仅关键字参数的默认值,以字典的形式返回,如果没有,那就返回None.

```python
print(func.__code__)
```

他会返回一个code对象,获取函数的代码对象,包含函数编译后的字节码以及相关信息.

```python
print(func.__code__.co_argcount)
```

他会计算函数定义的位置参数的数量,不包括\*args和\*\*kwargs.

```python
print(func.__code__.co_varnames)
```

获取函数中所有局部变量名的元组,包括传入的参数名和内部定义的变量.如果我们希望查找函数的其他属性,那么可以用dir函数来查看函数的具体属性.

Python中提供了inspect模块,用于在运行时获取对象的内部信息.

```python
import inspect
def func(a,b=10,*args,**kwargs):
    pass
# 获取函数签名
sig=inspect.signature(func)
print(sig)
# 获取参数信息
for name,param in sig.parameters.items():
    print(f"{name}: {param.default}")
```

这是inspect最为核心的功能之一.inspect.signature获取可调用对象(如函数)的签名对象.它包含了函数的参数名,默认值以及类型注解等信息.sig.parameters.items遍历签名中的所有参数.param.default获取参数的默认值,如果参数没有默认值,那么就会返回<class 'inspect.\_empty'>

```python
import inspect
import sys
# 定义测试对象
def my_function(x, y):
    return x + y
class MyClass:
    def instance_method(self):
        pass
    @classmethod
    def class_method(cls):
        pass
    @staticmethod
    def static_method():
        pass
my_instance = MyClass()
# 内置模块和函数
import math
# 执行类型检查
print("=" * 50)
print("inspect 类型检查函数验证")
print("=" * 50)
print(f"\n1. inspect.isfunction(my_function):")
print(f"   结果: {inspect.isfunction(my_function)}")
print(f"   说明: my_function 是普通函数 ✓")
print(f"\n2. inspect.isclass(MyClass):")
print(f"   结果: {inspect.isclass(MyClass)}")
print(f"   说明: MyClass 是类 ✓")
print(f"\n3. inspect.ismodule(sys):")
print(f"   结果: {inspect.ismodule(sys)}")
print(f"   说明: sys 是模块 ✓")
print(f"\n4. inspect.ismethod(my_instance.instance_method):")
print(f"   结果: {inspect.ismethod(my_instance.instance_method)}")
print(f"   说明: 绑定到实例的方法是方法 ✓")
print(f"\n5. inspect.isbuiltin(len):")
print(f"   结果: {inspect.isbuiltin(len)}")
print(f"   说明: len 是内置函数 ✓")
# 补充对比测试
print("\n" + "=" * 50)
print("补充对比测试")
print("=" * 50)
print(f"\ninspect.isfunction(MyClass.instance_method):")
print(f"   结果: {inspect.isfunction(MyClass.instance_method)}")
print(f"   说明: 未绑定的类方法是函数")
print(f"\ninspect.isfunction(my_instance.static_method):")
print(f"   结果: {inspect.isfunction(my_instance.static_method)}")
print(f"   说明: 静态方法被视为函数")
print(f"\ninspect.ismethod(MyClass.class_method):")
print(f"   结果: {inspect.ismethod(MyClass.class_method)}")
print(f"   说明: 类方法也是方法")
print(f"\ninspect.isbuiltin(math.sqrt):")
print(f"   结果: {inspect.isbuiltin(math.sqrt)}")
print(f"   说明: math.sqrt 是内置函数")
# 批量检查示例
print("\n" + "=" * 50)
print("批量类型检查示例")
print("=" * 50)
objects = {
    '普通函数': my_function,
    '类': MyClass,
    '实例方法': my_instance.instance_method,
    '类方法': MyClass.class_method,
    '静态方法': my_instance.static_method,
    '内置函数': len,
    '模块': sys,
    '字符串': "hello",
    '整数': 42,
}
for name, obj in objects.items():
    checks = {
        'isfunction': inspect.isfunction(obj),
        'ismethod': inspect.ismethod(obj),
        'isclass': inspect.isclass(obj),
        'ismodule': inspect.ismodule(obj),
        'isbuiltin': inspect.isbuiltin(obj),
    }
    result = ', '.join([k for k, v in checks.items() if v])
    print(f"{name:10s}: {result if result else '无匹配类型'}")
```

inspect模块中存在很多is开头的函数,用于验证对象是否为所需要的类型.

```python
# 获取源代码（字符串）
source = inspect.getsource(func)
# 获取源文件路径
file_path = inspect.getfile(func)
# 获取代码行号
line_no = inspect.getsourcelines(func)[1]
print(source)
print(file_path)
print(line_no)
```

它可以用于反查代码的物理位置和具体内容.getsource返回函数定义的源代码字符串.只能用于Python编写的函数,不能用于内置函数或交互式命令行中定义的函数.getfile返回定义该对象的文件路径.getsourcelines返回一个元组(source\_lines,start\_line\_no).这里的函数必须是用户自定义的函数.

```python
sig = inspect.signature(func)
args = (1, 2)
kwargs = {'c': 10}
bound = sig.bind(*args, **kwargs)
for name, val in bound.arguments.items():
    print(name, '=', val)
```

在不实际执行函数的情况下,模拟参数传递过程,检查参数是否匹配.sig.bind(\*args, \*\*kwargs):尝试将提供的参数绑定到函数签名上.其作用是验证参数,如果参数数量不对或名称错误,会抛出TypeError,而不会执行函数体;获取最终参数映射,bound.arguments是一个有序字典,显示了每个参数名最终对应的值,包括默认值填充.


<a id="org32735cf"></a>

## Eval/Exec

eval(expr)用于计算一个表达式的值.

```python
x=10
expr='3*x-2'
print(eval(expr))
```

exec(code)用于执行任意的函数语句.

```python
exec('for i in range(10): print(i)')
```

这些代码会在globals或locals中执行.区别在于eval只能处理单个表达式并且返回值,exec可以处理任意语句块(如循环,定义类),但不返回值,会返回None.动态编程指允许程序在运行时生成并执行代码.注意在exec的执行不会影响局部作用域.

```python
def func():
    x=15
    exec('x=10;print(x)')
    print(x)
func()
```

eval和exec的语法结构如下:

```python
eval(expr[,globals[,locals]])
exec(code[,globals[,locals]])
```

所以这样我们可以用exec修改局部变量的结构如下所示:

```python
def foo():
    x=15
    loc=locals()
    exec('x=10;print(x)',globals(),loc)
    x=loc['x']
    print(x)
```

在Python函数内部为了速度,优化了局部变量的存储,exec试图修改局部字典,但无法同步到优化的局部变量存储.从locals读取结果,应该避免这样的代码错误,不可靠且难以理解.对于eval/exec,极小心使用这类功能,存在不可对输入潜在安全问题.


<a id="org2b3edc1"></a>

## Callable Object

对于函数而言,我们可以定义自己的对象来模拟Python的函数(如callables),但必须实现call特殊方法.故而func调用的本质是调用func.\_\_call\_\_().

```python
class Memoize:
    def __init__(self,func):
        self._cache={}
        self._func=func
    def __call__(self,*args):
        if args in self._cache:
            return self._cache[args]
        r=self._func(*args)
        self._cache[args]=r
        return r
    def clear(self):
        self._cache.clear()
@Memoize  # 等同于 fib = Memoize(fib)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
# 调用时完全像普通函数
print(fib(10)) 
fib.clear()  # 清除缓存，这是普通函数做不到的
```

