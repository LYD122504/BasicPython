import inspect
from functools import wraps
class Validator:
    def __init__(self,name=None):
        self.name=name
    validators={}
    def __init_subclass__(cls):
        cls.validators[cls.__name__]=cls
    @classmethod
    def check(cls,value):
        return value
    def __set_name__(self,cls,name):
        self.name=name
    def __set__(self,instance,value):
        instance.__dict__[self.name]=self.check(value)
class Typed(Validator):
    expected_type=object
    @classmethod
    def check(cls,value):
        if not isinstance(value,cls.expected_type):
            raise TypeError(f'Expected{cls.expected_type}')
        return super().check(value)
_typed_classes=[
    ('Integer',int),
    ('Float',float),
    ('String',str)
]
globals().update((name, type(name, (Typed,), {'expected_type':ty}))
                 for name, ty in _typed_classes)
class Positive(Validator):
    @classmethod
    def check(cls,value):
        if value<0:
            raise ValueError('Expected >=0')
        return super().check(value)
class NotEmpty(Validator):
    @classmethod
    def check(cls,value):
        if len(value)==0:
            raise ValueError('Must be non-empty')
        return super().check(value)
class PositiveInteger(Integer,Positive):
    pass
class PositiveFloat(Float,Positive):
    pass
class NonEmptyString(String,NotEmpty):
    pass
class ValidatedFunction:
    def __init__(self,func):
        self.func=func
    def __call__(self,*args,**kwargs):
        sig=inspect.signature(self.func)
        bound=sig.bind(*args,**kwargs)
        annotations=self.func.__annotations__
        for name,val in bound.arguments.items():
            if name in annotations:
                expected_test=annotations[name]
                expected_test.check(val) 
        print('Calling',self.func)
        result=self.func(*args,**kwargs)
        return result
def validated(func):
    sig=inspect.signature(func)
    annotations=dict(func.__annotations__)
    return_check=annotations.pop('return',None)
    @wraps(func)
    def wrapper(*args,**kwargs):
        bound=sig.bind(*args,**kwargs)
        errors=[]
        for name,validator in annotations.items():
            try:
                validator.check(bound.arguments[name])
            except Exception as e:
                 errors.append(f'    {name}: {e}')
        if errors:
            raise TypeError('Bad Arguments\n' + '\n'.join(errors))
        print('Calling',func)
        result=func(*args,**kwargs)
        # Enforce return check (if any)
        if return_check:
            try:
                return_check.check(result)
            except Exception as e:
                raise TypeError(f'Bad return: {e}') from None
        return result
    return wrapper
def enforce(**annotations):
    return_check=annotations.pop('return_c',None)
    def validated(func):
        sig=inspect.signature(func)
        @wraps(func)
        def wrapper(*args,**kwargs):
            bound=sig.bind(*args,**kwargs)
            errors=[]
            for name,validator in annotations.items():
                try:
                    validator.check(bound.arguments[name])
                except Exception as e:
                    errors.append(f'    {name}: {e}')
            if errors:
                raise TypeError('Bad Arguments\n' + '\n'.join(errors))
            print('Calling',func)
            result=func(*args,**kwargs)
            # Enforce return check (if any)
            if return_check:
                try:
                    return_check.check(result)
                except Exception as e:
                    raise TypeError(f'Bad return: {e}') from None
            return result
        return wrapper
    return validated