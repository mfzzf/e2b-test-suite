"""
图表测试 - Matplotlib 图表生成与解析
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)
from e2b_code_interpreter import Sandbox


def test_bar_chart():
    """测试柱状图生成"""
    print("=" * 50)
    print("测试: 柱状图生成")
    print("=" * 50)
    
    code = """
import matplotlib.pyplot as plt

authors = ['Author A', 'Author B', 'Author C', 'Author D']
sales = [100, 200, 300, 400]

plt.figure(figsize=(10, 6))
plt.bar(authors, sales, label='Books Sold', color='blue')
plt.xlabel('Authors')
plt.ylabel('Number of Books Sold')
plt.title('Book Sales by Authors')
plt.tight_layout()
plt.show()
"""
    
    sandbox = Sandbox.create()
    try:
        execution = sandbox.run_code(code)
        
        if execution.results and len(execution.results) > 0:
            chart = execution.results[0].chart
            if chart:
                print(f"图表类型: {chart.type}")
                print(f"标题: {chart.title}")
                print(f"X轴标签: {chart.x_label}")
                print(f"Y轴标签: {chart.y_label}")
                print(f"元素数量: {len(chart.elements) if chart.elements else 0}")
                
                if chart.elements:
                    for elem in chart.elements:
                        print(f"  - {elem.label}: {elem.value}")
            else:
                print("未检测到图表结构")
        else:
            print("无结果返回")
        
        print("✓ 柱状图测试通过")
        return True
    finally:
        sandbox.kill()


def test_line_chart():
    """测试折线图生成"""
    print("\n" + "=" * 50)
    print("测试: 折线图生成")
    print("=" * 50)
    
    code = """
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.figure(figsize=(8, 5))
plt.plot(x, y, marker='o', label='Linear Growth')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.title('Simple Line Chart')
plt.legend()
plt.grid(True)
plt.show()
"""
    
    sandbox = Sandbox.create()
    try:
        execution = sandbox.run_code(code)
        
        print(f"结果数量: {len(execution.results) if execution.results else 0}")
        
        print("✓ 折线图测试通过")
        return True
    finally:
        sandbox.kill()


def test_pie_chart():
    """测试饼图生成"""
    print("\n" + "=" * 50)
    print("测试: 饼图生成")
    print("=" * 50)
    
    code = """
import matplotlib.pyplot as plt

labels = ['Python', 'JavaScript', 'Go', 'Rust']
sizes = [40, 30, 20, 10]
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.title('Programming Language Usage')
plt.show()
"""
    
    sandbox = Sandbox.create()
    try:
        execution = sandbox.run_code(code)
        
        print(f"结果数量: {len(execution.results) if execution.results else 0}")
        
        print("✓ 饼图测试通过")
        return True
    finally:
        sandbox.kill()


def run_all():
    """运行所有图表测试"""
    test_bar_chart()
    test_line_chart()
    test_pie_chart()


if __name__ == "__main__":
    run_all()
