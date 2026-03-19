import unittest
import stock

class TestStock(unittest.TestCase):
    def test_create(self):
        s = stock.Stock('GOOG', 100, 490.1)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)
    def test_argument(self):
        s=stock.Stock(name='GOOG',shares=100,price=490.1)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)
    def test_cost(self):
        s=stock.Stock('GOOG',100,490.1)
        result=s.cost
        self.assertEqual(result,49010)
    def test_sell(self):
        s=stock.Stock('GOOG',100,490.1)
        self.assertEqual(s.shares,100)
        s.sell(75)
        self.assertEqual(s.shares,25)
    def test_from_row(self):
        s = stock.Stock.from_row(['GOOG','100','490.1'])
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)
    def test_repr(self):
        s = stock.Stock.from_row(['GOOG','100','490.1'])
        self.assertEqual(repr(s),"Stock(GOOG,100,490.1)")
    def test_eq(self):
        s1 = stock.Stock.from_row(['GOOG','100','490.1']) 
        s2 = stock.Stock.from_row(['GOOG','100','490.1'])
        self.assertTrue(s1==s2)
    def test_bad_shares(self):
        s=stock.Stock('GOOG',100,490.1)
        # 在下面的代码块中必须要抛出一个TypeError异常
        # 如果未抛出或抛出其他类型的异常,那么测试就会失败
        with self.assertRaises(TypeError):
            s.shares='50'
    def test_negative_shares(self):
        s=stock.Stock('GOOG',100,490.1)
        with self.assertRaises(ValueError):
            s.shares=-50
    def test_bad_price(self):
        s=stock.Stock('GOOG',100,490.1)
        with self.assertRaises(TypeError):
            s.price='20'
    def test_negative_price(self):
        s=stock.Stock('GOOG',100,490.1)
        with self.assertRaises(ValueError):
            s.price=-50.0
    def test_attribute(self):
        s=stock.Stock('GOOG',100,490.1)
        with self.assertRaises(AttributeError):
            s.share=-50
if __name__ == '__main__':
    unittest.main()