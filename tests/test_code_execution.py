"""
代码执行测试 - Python 代码在沙箱中执行
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)
from e2b_code_interpreter import Sandbox


def test_simple_code():
    """测试简单代码执行"""
    print("=" * 50)
    print("测试: 简单代码执行")
    print("=" * 50)
    
    sbx = Sandbox.create()
    
    execution = sbx.run_code("print('hello world')")
    print(f"输出: {execution.logs}")
    
    assert "hello world" in str(execution.logs), "输出不包含预期内容"
    
    sbx.kill()
    print("✓ 简单代码执行测试通过")
    return True


def test_math_calculation():
    """测试数学计算"""
    print("\n" + "=" * 50)
    print("测试: 数学计算")
    print("=" * 50)
    
    sbx = Sandbox.create()
    
    code = """
import math
result = math.sqrt(144) + math.pow(2, 10)
print(f"计算结果: {result}")
result
"""
    execution = sbx.run_code(code)
    print(f"输出: {execution.logs}")
    print(f"结果: {execution.results}")
    
    sbx.kill()
    print("✓ 数学计算测试通过")
    return True


def test_data_processing():
    """测试数据处理"""
    print("\n" + "=" * 50)
    print("测试: 数据处理")
    print("=" * 50)
    
    sbx = Sandbox.create()
    
    code = """
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
avg = sum(data) / len(data)
max_val = max(data)
min_val = min(data)
print(f"平均值: {avg}, 最大值: {max_val}, 最小值: {min_val}")
"""
    execution = sbx.run_code(code)
    print(f"输出: {execution.logs}")
    
    sbx.kill()
    print("✓ 数据处理测试通过")
    return True


def test_error_handling():
    """测试错误处理"""
    print("\n" + "=" * 50)
    print("测试: 错误处理")
    print("=" * 50)
    
    sbx = Sandbox.create()
    
    code = """
# 故意制造错误
x = 1 / 0
"""
    execution = sbx.run_code(code)
    print(f"错误: {execution.error}")
    
    assert execution.error is not None, "应该有错误"
    
    sbx.kill()
    print("✓ 错误处理测试通过")
    return True


def run_all():
    """运行所有代码执行测试"""
    test_simple_code()
    test_math_calculation()
    test_data_processing()
    test_error_handling()


if __name__ == "__main__":
    run_all()
