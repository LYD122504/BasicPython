from .models import PhysicalProduct,PRODUCT_REGISTRY
import csv
from collections import Counter,deque
from functools import wraps

def coroutine(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        cr=func(*args,**kwargs)
        cr.send(None)
        return cr
    return wrapper

@coroutine
def stock_filter(manager,target_coroutine):
    while True:
        order=yield
        if manager.stock_counter[order['name']]>=order['qty']:
            target_coroutine.send(order)
        else:
            print('库存不足,处理失败')

@coroutine
def order_processor(manager):
    while True:
        order=yield
        manager.stock_counter[order['name']]-=order['qty']
        print('成功处理')

def read_csv_lazily(filename):
    with open(filename,'r',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        for row in reader:
            yield row

class InventoryTransaction(object):
    def __init__(self,manager,product_name,qty):
        self.manager=manager
        self.product_name=product_name
        self.qty=qty
    def __enter__(self):
        # 预扣
        self.manager.stock_counter[self.product_name]-=self.qty
        print(f"事务开始：预扣减 {self.qty} 件 {self.product_name}")
        return self
    def __exit__(self,exc_type,exc_val,exc_tb):
        if exc_type is not None:
            self.manager.stock_counter[self.product_name] += self.qty
            print(f"事务失败：检测到异常 {exc_type.__name__}，库存已自动回滚！")
        else:
            print("事务提交：订单处理彻底完成！")
from .models import PhysicalProduct, PRODUCT_REGISTRY
import csv
from collections import Counter, deque
from functools import wraps

# ... (coroutine, stock_filter, order_processor, read_csv_lazily 逻辑保持不变) ...

class InventoryManager(object):
    def __init__(self):
        self.products = {}
        self.stock_counter = Counter()
        self.history = deque(maxlen=5)

    def add_product(self, name, price, stock, extra_val, others, Pclass):
        """统一入库接口"""
        try:
            # 这里的实例化顺序必须与 models.py 严格一致
            product = Pclass(name, price, stock, extra_val, others)
            self.products[name] = product
            self.stock_counter[name] += stock
            self.history.append(f'成功入库:{name}')
        except (ValueError, TypeError, Exception) as e:
            self.history.append(f'入库失败:{name}, 原因: {e}')

    def load_from_generator(self, filename):
        for row in read_csv_lazily(filename):
            try:
                # 提取核心字段
                p_type = row.pop('type')
                ProductClass = PRODUCT_REGISTRY[p_type]
                
                name = row.pop('name')
                price = float(row.pop('price'))
                stock = int(row.pop('stock'))
                # 兼容不同来源的 CSV 列名
                extra_val = float(row.pop('extra_attr', 0.0) or row.pop('weight', 0.0))
                
                # 此时 row 字典里只剩下 brand 等额外字段了，直接作为 others
                others = row 
                
                self.add_product(name, price, stock, extra_val, others, ProductClass)
            except KeyError as e:
                self.history.append(f'加载跳过：缺少必要列 {e}')
            except Exception as e:
                self.history.append(f'入库意外错误: {e}')

    def load_from_csv(self, filename):
        """修正版：补齐 others 参数"""
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    name = row['name']
                    price = float(row['price'])
                    stock = int(row['stock'])
                    weight = float(row.get('weight', 0.0) or row.get('extra_attr', 0.0))
                    # 传入空字典作为 others 占位
                    self.add_product(name, price, stock, weight, {}, PhysicalProduct)
                except Exception as e:
                    self.history.append(f'CSV解析错误: {e}')

    # --- 第11关：容器协议 ---
    def __len__(self):
        return len(self.products)

    def __getitem__(self, key):
        return self.products[key]

    def __iter__(self):
        # 迭代器协议：直接产出商品对象
        yield from self.products.values()

__all__ = ['InventoryTransaction', 'InventoryManager']