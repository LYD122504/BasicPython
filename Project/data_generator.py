import csv
import random

def generate_concurrency_data(filename='concurrency_test.csv', count=5000):
    header = ['type', 'name', 'price', 'stock', 'extra_attr', 'brand', 'tax_rate']
    types = ['Physical', 'Digital', 'LuxuryFresh']
    
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(count):
            writer.writerow([
                random.choice(types),
                f"Product_{i}",
                round(random.uniform(10, 10000), 2),
                random.randint(1, 100),
                round(random.uniform(0.1, 5.0), 2),
                "Brand_X",
                0.15
            ])
    print(f"✅ 成功生成 {count} 条并发测试数据！")

if __name__ == '__main__':
    generate_concurrency_data()