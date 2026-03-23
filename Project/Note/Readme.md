# 🚀 Smart-Inventory-Engine

**基于 Python 高级特性构建的工业级并发库存处理引擎**

# 🌟 项目核心亮点

本项目严格遵循 **David Beazley** 的 Python 进阶思想，通过 15 个渐进式挑战，将 Python 的动态性、内存管理和并发能力压榨到了极致。它不只是一个简单的 CRUD 应用，而是一套探索 Python 底层机制的架构实验。

------

# 🏗️ 核心架构技术栈

## 模型层 (Modeling)

- **元类约束 (Metaclasses)**：利用 `StrictModelMeta` 强制执行开发规范，确保所有商品模型必须包含 `__slots__` 和 `Docstring`。
- **数据描述符 (Descriptors)**：自定义 `PositiveNumber` 描述符，实现非侵入式的类型检查和数值校验，从底层杜绝非法库存数据。
- **内存优化 (Memory Efficiency)**：全量使用 `__slots__` 消除 `__dict__` 开销，支持在极低内存占用下处理 10 万级数据。

##  动态扩展与协议 (Dynamic Protocols)

- **混入模式 (Mixins)**：通过 `TaxableMixin` 和 `ExpirableMixin` 实现功能的“即插即用”，完美解决多重继承下的 MRO (方法解析顺序) 问题。
- **属性拦截器 (`__getattr__`)**：构建动态属性代理，将非核心业务字段（如品牌、产地）自动分流至扩展字典，保持核心模型精简。
- **魔法方法 (Magic Methods)**：重写对象协议，支持原生容器操作（`len`, `iter`, `getitem`）以及基于价格的自动排序 (`__lt__`)。

## 函数式与异步流水线 (Functional Pipeline)

- **闭包工厂 (Closures)**：实现 `make_discount_calculator` 闭包，支持动态生成带有状态的促销折扣逻辑。
- **协程流水线 (Coroutines)**：利用装饰器封装协程，构建了 `stock_filter -> order_processor` 的非阻塞处理流。
- **上下文管理器 (Context Managers)**：实现 `InventoryTransaction` 事务机制，通过 `__enter__` 和 `__exit__` 确保订单处理失败时库存自动回滚。

## 高性能并发 (Concurrency)

- **执行池 (Executors)**：集成 `ThreadPoolExecutor`，利用多线程并发处理大规模折扣计算，在 I/O 密集型场景下实现数倍的性能提升。
- **惰性加载 (Lazy Loading)**：通过生成器（Generator）按需读取大数据集，避免内存溢出。

------

# 📂 项目结构

```
smart_inventory/
├── models.py       # 核心模型、元类、描述符、Mixins
├── manager.py      # 仓库管理器、协程流、事务处理器
├── utils.py        # 闭包折扣引擎、并发批处理器
└── __main__.py     # 综合集成测试与性能跑分
```

------

# 🧪 如何运行压力测试

1. **生成数据**：运行数据生成脚本创建 `mix.csv`。

2. **启动引擎**：

   ```
   python -m smart_inventory
   ```

3. **观察输出**：系统将自动展示 MRO 链路、事务回滚效果、动态属性拦截以及并发处理的加速比。