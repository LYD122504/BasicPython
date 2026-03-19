import inspect
import sys
from validate import Validator,validated
from collections import ChainMap
def validate_attributes(cls):
    validators=[]
    for name,val in vars(cls).items():
        if isinstance(val,Validator):
            validators.append(val)
        elif callable(val) and val.__annotations__:
            setattr(cls,name,validated(val))
    cls._fields = [val.name for val in validators]
    cls._types = tuple([ getattr(v, 'expected_type', lambda x: x)
                   for v in validators ])
    cls.create_init()
    return cls
class StructureMeta(type):
    @classmethod
    # 第一个参数{}是一个空字典,用来存放类主体中新定义的属性,避免污染验证器字典
    def __prepare__(meta,clsname,bases):
        return ChainMap({},Validator.validators)
    @staticmethod
    def __new__(meta,clsname,bases,methods):
        # 只保留用户在类主体中显式定义的属性，剔除 Validator.validators 中的全局内容。如果不这样做，最终创建的类字典里会混入所有全局验证器，导致污染。
        methods=methods.maps[0]
        # maps是Chainmap的元组,包含构成ChainMap链的映射对象
        return super().__new__(meta,clsname,bases,methods)
class Structure(metaclass=StructureMeta):
    _types=()
    def __iter__(self):
        for name in self._fields:
            yield getattr(self,name)
    @classmethod
    def from_row(cls,row):
        rowdata = [ func(val) for func, val in zip(cls._types, row) ]
        return cls(*rowdata)
    def __init_subclass__(cls):
        validate_attributes(cls)
    @classmethod
    def create_init(cls):
        argstr=','.join(cls._fields)
        code = f'def __init__(self, {argstr}):\n'
        for name in cls._fields:
            code+=f'    self.{name}={name}\n'
        locs={ }
        exec(code,locs)
        cls.__init__=locs['__init__']
    @classmethod
    def set_fields(cls):
        sig=inspect.signature(cls.__init__)
        cls._fields=tuple(sig.parameters)
    @staticmethod
    def _init():
        locs=sys._getframe(1).f_locals # Get callers local variables
        self = locs['self']
        for name, val in locs.items():
            if name == 'self': continue
            setattr(self, name, val)
    def __repr__(self):
        result=''
        for i in range(len(self._fields)):
            result+=str(getattr(self,self._fields[i]))
            if i!=len(self._fields)-1:
                result+=','
        return f'{self.__class__.__name__}({result})'
    def __setattr__(self, name, value):
        if name[0]!='_' and name not in self._fields:
            raise AttributeError('No attribute %s' % name)
        super().__setattr__(name, value)
    def __eq__(self,other):
        return isinstance(other,type(self)) and tuple(self)==tuple(other)
def typed_structure(clsname,**validators):
    cls=type(clsname,(Structure,),validators)
    return cls
