from .manager import InventoryManager, InventoryTransaction
from .manager import order_processor, stock_filter
from smart_inventory import *
import time

manager = InventoryManager()
# 假设你的 CSV 文件名是 products.csv
manager.load_from_generator('mix.csv')

print("\n--- 历史操作记录 (由于 deque(maxlen=5)，这里只显示最后5条) ---")
for log in manager.history:
    print(log)
    
print("\n--- 当前库存统计排名 (前3名) ---")
# Counter 提供了一个非常方便的 most_common 方法！
for name, count in manager.stock_counter.most_common(3):
    print(f"{name}: {count} 件")
# ==========================================
# 任务 4：连接流水线并注入测试订单
# ==========================================
print("\n--- 启动协程订单处理流水线 ---")

processor = order_processor(manager)
pipeline = stock_filter(manager, processor)

incoming_orders = [
    {'name': 'MacBook Pro', 'qty': 2},          # 正常订单，库存充裕
    {'name': 'Nintendo Switch', 'qty': 200},    # ❌ 超卖订单！CSV里库存只有120，应该被拦截
    {'name': '黑神话悟空激活码', 'qty': 10},    # 正常订单，虚拟商品
    {'name': 'MacBook Pro', 'qty': 50},         # ❌ 叠加超卖！刚才买走2台剩48，现在要50，应该被拦截
]

print("开始接收前端订单流...")
for order in incoming_orders:
    print(f"收到请求: 尝试购买 {order['qty']} 件 [{order['name']}]")
    pipeline.send(order)
    
print("\n--- 订单处理完毕，最终库存快照 ---")
for name, count in manager.stock_counter.most_common(3):
    print(f"{name}: {count} 件")

print("\n=== 第八关测试：上下文管理器与事务回滚 ===")
# 假设 manager 里已经有了 MacBook，库存假设为 100
manager.stock_counter['MacBook'] = 100
print(f"当前 MacBook 库存: {manager.stock_counter['MacBook']}")

try:
    with InventoryTransaction(manager, 'MacBook', 2):
        print("正在处理支付...")
        # 一切顺利，自然结束
except Exception as e:
    print(e)
print(f"正常购买后库存: {manager.stock_counter['MacBook']}")

try:
    with InventoryTransaction(manager, 'MacBook', 5):
        print("正在处理支付...")
        raise ConnectionError("网络突然断开，支付失败！") # 模拟程序崩溃
except ConnectionError as e:
    print(f"前端捕获到错误: {e}")
print(f"崩溃回滚后库存 (应该仍然是98，而不是93): {manager.stock_counter['MacBook']}")

print("\n" + "="*40)
print("🚀 第 11 关：对象协议 (Magic Methods) 验收")
print("="*40)

# 1. 测试 __len__ (容器协议)
print(f"📊 当前仓库品类总数: {len(manager)}")

# 2. 测试 __getitem__ 和 __repr__ (表现协议)
# 注意：我们现在可以直接通过 manager['名字'] 访问了，不需要通过 manager.products['名字']
try:
    # 获取第一个商品的名字用于测试
    first_name = list(manager.products.keys())[0]
    sample_p = manager[first_name] 
    print(f"🔍 抽检商品详情 (自动触发 __repr__): {sample_p}") 
except (IndexError, KeyError):
    print("仓库为空，请检查 CSV 加载情况")

# 3. 测试迭代协议与排序 (基于 __lt__)
print("\n💰 仓库商品价格排行榜 (从低到高):")
# 只要实现了 __iter__，manager 就是可迭代对象
# 只要实现了 __lt__，sorted 就能直接对 manager 进行排序
for p in sorted(manager): 
    print(f"  - {p.name:20} | 价格: {p.price:>8.2f} 元")

# 4. 测试比较运算符
if len(manager) >= 2:
    prods = sorted(manager)
    print(f"\n⚖️ 价格对比测试: {prods[0].name} 是否比 {prods[-1].name} 便宜? {prods[0] < prods[-1]}")

# 1. 模拟一个带额外属性的商品
# 假设我们手动给第一个商品塞了一个 'brand' 属性到它的 _extra_data 里
print("\n" + "="*40)
print("🚀 第 12 关：动态属性代理 (__getattr__) 深度验收")
print("="*40)

# 加载刚才生成的 5 条精选数据
manager.load_from_generator('mix.csv')

if len(manager) > 0:
    # 拿取 MacBook Pro 进行测试
    p = manager['MacBook Pro']
    
    print(f"📦 商品名称 (核心属性): {p.name}")
    print(f"💰 商品价格 (核心属性): {p.price}")
    
    # 下面这些属性在类定义里压根没有，全是动态拦截出来的！
    print(f"🔹 品牌 (动态拦截): {p.brand}")
    print(f"🔹 颜色 (动态拦截): {p.color}")
    print(f"🔹 产地 (动态拦截): {p.origin}")
    print(f"🔹 材质 (动态拦截): {p.material}")
    
    # 测试完全不存在的属性
    try:
        print(p.non_existent_field)
    except AttributeError as e:
        print(f"✅ 捕获预期错误: {e}")
else:
    print("数据加载失败，请检查 mix.csv")
print("\n" + "="*40)
print("🚀 第 13 关：多重继承与 Mixins 验收")
print("="*40)
# 加载刚才生成的 5 条精选数据
manager.load_from_generator('mix_MRO.csv')
# 1. 找到 LuxuryFresh 商品
luxury_prods = [p for p in manager if p.__class__.__name__ == 'LuxuryFreshProduct']

if luxury_prods:
    item = luxury_prods[0]
    print(f"📦 测试对象: {item.name}")
    
    # 2. 测试 TaxableMixin 功能
    print(f"  💰 原价: {item.price} | 含税价: {item.get_taxed_price()} (税率: {item.tax_rate})")
    
    # 3. 测试 ExpirableMixin 功能
    status = "❌ 已过期" if item.is_expired() else "✅ 新鲜"
    print(f"  📅 保质期: {item.expiry_date} | 状态: {status}")

    # 4. 打印 MRO (本关核心考点)
    print("\n🔍 继承链路 (MRO):")
    for i, cls in enumerate(item.__class__.mro()):
        print(f"  [{i}] {cls.__name__}")
else:
    print("未发现 LuxuryFresh 商品，请检查 mix.csv 和注册逻辑。")
print("\n" + "="*40)
print("🚀 第 14 关：闭包与动态折扣引擎验收")
print("="*40)

# 1. 生产一个“满 5000 打 8 折”的计算器
luxury_discount = make_discount_calculator(5000, 0.8)

# 2. 找两个商品对比
p_expensive = manager['MacBook Pro']  # 14999 元
p_normal = manager['Nintendo Switch'] # 2299 元

print(f"💎 {p_expensive.name} 原价: {p_expensive.price} -> 促销价: {luxury_discount(p_expensive)}")
print(f"🎮 {p_normal.name} 原价: {p_normal.price} -> 促销价: {luxury_discount(p_normal)} (未达标)")

# 3. 硬核内省：拆解闭包
print("\n🔍 正在通过 __closure__ 属性探测闭包内存...")
if luxury_discount.__closure__:
    # 闭包里的变量存储在 cell 对象中
    captured_values = [cell.cell_contents for cell in luxury_discount.__closure__]
    print(f"  📦 闭包捕获的自由变量: {captured_values}")

# 4. 验证函数名
print(f"  🏷️ 函数名称: {luxury_discount.__name__}")

# 1. 加载 5000 条大数据
manager.load_from_generator('concurrency_test.csv')
all_prods = list(manager) # 获取所有商品实例
discount_logic = make_discount_calculator(1000, 0.8)

print(f"\n🚀 开始对 {len(all_prods)} 件商品进行折扣批处理...")

# 2. 传统单线程循环
start_time = time.perf_counter()
serial_results = [process_single_discount(p, discount_logic) for p in all_prods]
serial_duration = time.perf_counter() - start_time
print(f"⏱️  单线程耗时: {serial_duration:.4f} 秒")

# 3. 多线程并发 (10个工人)
start_time = time.perf_counter()
concurrent_results = batch_process_concurrently(all_prods, discount_logic, workers=20)
concurrent_duration = time.perf_counter() - start_time
print(f"⚡ 多线程耗时: {concurrent_duration:.4f} 秒 (提升 {serial_duration/concurrent_duration:.1f} 倍)")

# 4. 验证数据准确性
assert serial_results == concurrent_results
print("✅ 结果完全一致，并发处理成功！")