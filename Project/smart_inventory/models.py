from abc import ABC,abstractmethod,ABCMeta
from datetime import datetime

class PositiveNumber(object):
    def __init__(self,expected_type,flag=True):
        self.type=expected_type
        self.flag=flag
    def __set_name__(self,owner,name):
        self.name='_'+name
    def __get__(self,instance,owner):
        if instance is None:
            return self
        return getattr(instance,self.name)
    def __set__(self,instance,val):
        if not isinstance(val,self.type):
            raise TypeError('Excepted a digit')
        if self.flag and val<0:
            raise ValueError('Excepted a positive number')
        setattr(instance,self.name,val)

class TaxableMixin(object):
    def get_taxed_price(self):
        return round(self.price * (1 + float(self.tax_rate)), 2)

class ExpirableMixin(object):
    def is_expired(self):
        expiry_date=datetime.strptime(self.expiry_date,'%Y-%m-%d')
        return expiry_date<datetime.now()

PRODUCT_REGISTRY={}
def register_product(product_type):
    def decorator(cls):
        PRODUCT_REGISTRY[product_type] = cls
        return cls
    return decorator

class StrictModelMeta(ABCMeta):
    def __new__(mcs,name,bases,namespace):
        if name=='BaseProduct':
            pass
        else:
            if '__slots__' not in namespace:
                raise TypeError(f"类 {name} 必须定义 __slots__ 以优化内存!")
            if '__doc__' not in namespace:
                raise TypeError(f"类 {name} 必须包含类文档注释 (Docstring)!")
        return super().__new__(mcs,name,bases,namespace)
    
class BaseProduct(ABC,metaclass=StrictModelMeta):
    __slots__=['_name','_price','_extra_data']
    price=PositiveNumber((int,float))
    @abstractmethod
    def get_description(self):
        pass
    def __init__(self,name,price,extra_data=None):
        self._name=name
        self.price=price
        self._extra_data=extra_data
    @property
    def name(self):
        return self._name
    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}, ￥{self.price}>"
    def __eq__(self,other):
        return isinstance(other,BaseProduct) and (self.price==other.price)
    def __lt__(self, other):
       return isinstance(other,BaseProduct) and (self.price<other.price) 
    def __getattr__(self, name):
        if name in self._extra_data:
            return self._extra_data[name]
        else:
            raise AttributeError('Empty Attribute')
@register_product('Physical')   
class PhysicalProduct(BaseProduct):
    """实体商品类"""
    __slots__=['_stock','_weight']
    stock=PositiveNumber(int)
    weight=PositiveNumber((int,float))
    def __init__(self,name,price,stock,weight,others=None):
        super().__init__(name,price,others)
        self.stock=stock
        self.weight=weight
    def get_description(self):
        return f"Name: {self.name}; Price: {self.price}; Stock: {self.stock}; Weight: {self.weight}; "

@register_product('Digital')
class DigitalProduct(BaseProduct):
    """虚拟商品类"""
    __slots__=['_stock','_file_size']
    stock=PositiveNumber(int)
    file_size=PositiveNumber((int,float),False)
    def __init__(self,name,price,stock,weight,others=None):
        super().__init__(name,price,others)
        self.stock=stock
        self.file_size=weight
    def get_description(self):
        return f"Name: {self.name}; Price: {self.price}; Stock: {self.stock}; File size: {self.file_size}; "

@register_product('LuxuryFresh')
class LuxuryFreshProduct(ExpirableMixin, TaxableMixin, PhysicalProduct):
    '''税后生鲜'''
    __slots__=[]
__all__=['PRODUCT_REGISTRY','PhysicalProduct','DigitalProduct','LuxuryFreshProduct']