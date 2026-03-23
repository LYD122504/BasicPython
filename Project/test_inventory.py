import unittest
from smart_inventory import *
class TestModels(unittest.TestCase):
    def test_negative_stock_raises_error(self):
        p = PhysicalProduct("Test", 100, 10, 1.0)
        with self.assertRaises(ValueError):
            p.stock=-5
class TestManager(unittest.TestCase):
    def setUp(self):
        self.manager = InventoryManager()
        # 假设你的 CSV 文件名是 products.csv
        self.manager.load_from_generator('mix.csv')
        self.manager.stock_counter['MacBook'] = 100

    def test_transaction_rollback(self):
        try:
            with InventoryTransaction(self.manager, 'MacBook', 10):
                raise Exception("模拟断网")
        except Exception:
            pass
        self.assertEqual(self.manager.stock_counter['MacBook'],100)

if __name__ == '__main__':
    unittest.main()
            