from structure import Structure, validate_attributes
import sys
import validate
class Stock(Structure):
    _fields=('name','shares','price')
    name = String()
    shares = PositiveInteger()
    price = PositiveFloat()
    @property
    def cost(self):
        return self.shares * self.price
    def sell(self, nshares: PositiveInteger):
        self.shares -= nshares
