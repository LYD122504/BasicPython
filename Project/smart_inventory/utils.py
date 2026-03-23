import time
from concurrent.futures import ThreadPoolExecutor

def make_discount_calculator(threshold,rate):
    def calculator(product):
        if product.price>=threshold:
            return product.price*rate
        else:
            return product.price
    return calculator

def process_single_discount(product,discount_func):
    """模拟一个耗时的业务逻辑：计算折扣 + 模拟网络日志记录"""
    # 模拟 I/O 阻塞：比如把折扣结果同步到远程服务器
    time.sleep(0.001) 
    return discount_func(product)

def batch_process_concurrently(products, discount_func, workers=10):
    """使用线程池并行处理"""
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # map 会按顺序返回结果
        results = list(executor.map(lambda p: process_single_discount(p, discount_func), products))
    return results
__all__=['make_discount_calculator','process_single_discount','batch_process_concurrently']