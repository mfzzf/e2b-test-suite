"""
Code Interpreter 上下文管理测试 - 上下文创建、有状态执行、上下文管理
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)
from ucloud_sandbox.code_interpreter import Sandbox


def test_create_code_context():
    """测试创建代码执行上下文"""
    print("=" * 50)
    print("测试: 创建代码执行上下文")
    print("=" * 50)
    
    sbx = Sandbox.create()
    try:
        # 创建一个新的上下文
        context = sbx.create_code_context(language="python")
        print(f"上下文ID: {context.id}")
        print(f"语言: {context.language}")
        print(f"工作目录: {context.cwd}")
        
        assert context.id is not None, "上下文ID不应为空"
        assert context.language == "python", "语言应为python"
        
        # 列出所有上下文
        contexts = sbx.list_code_contexts()
        print(f"上下文数量: {len(contexts)}")
        
        assert len(contexts) >= 1, "应至少有一个上下文"
        
        print("✓ 创建代码执行上下文测试通过")
        return True
    finally:
        sbx.kill()


def test_stateful_execution():
    """测试有状态代码执行 - 变量在多次运行间保持"""
    print("\n" + "=" * 50)
    print("测试: 有状态代码执行")
    print("=" * 50)
    
    sbx = Sandbox.create()
    try:
        # 第一次执行：定义变量
        execution1 = sbx.run_code("x = 42")
        print(f"第一次执行: 定义 x = 42")
        
        # 第二次执行：使用之前定义的变量
        execution2 = sbx.run_code("y = x * 2\nprint(f'y = {y}')")
        print(f"第二次执行输出: {execution2.logs.stdout}")
        
        assert "84" in str(execution2.logs.stdout), "y 应该等于 84"
        
        # 第三次执行：继续使用变量
        execution3 = sbx.run_code("z = x + y\nz")
        print(f"第三次执行结果: {execution3.text}")
        
        assert execution3.text == "126", "z 应该等于 126"
        
        print("✓ 有状态代码执行测试通过")
        return True
    finally:
        sbx.kill()


def test_context_cwd():
    """测试自定义工作目录的上下文"""
    print("\n" + "=" * 50)
    print("测试: 自定义工作目录上下文")
    print("=" * 50)
    
    sbx = Sandbox.create()
    try:
        # 创建自定义工作目录
        sbx.commands.run("mkdir -p /tmp/test_dir")
        
        # 创建带有自定义工作目录的上下文
        context = sbx.create_code_context(cwd="/tmp/test_dir")
        print(f"上下文工作目录: {context.cwd}")
        
        assert context.cwd == "/tmp/test_dir", "工作目录应为 /tmp/test_dir"
        
        # 在该上下文中执行代码验证工作目录
        execution = sbx.run_code("import os; print(os.getcwd())", context=context)
        print(f"执行输出: {execution.logs.stdout}")
        
        assert "/tmp/test_dir" in str(execution.logs.stdout), "工作目录应包含 /tmp/test_dir"
        
        print("✓ 自定义工作目录上下文测试通过")
        return True
    finally:
        sbx.kill()


def test_remove_context():
    """测试移除上下文"""
    print("\n" + "=" * 50)
    print("测试: 移除上下文")
    print("=" * 50)
    
    sbx = Sandbox.create()
    try:
        # 创建一个新的上下文
        context = sbx.create_code_context()
        context_id = context.id
        print(f"创建上下文: {context_id}")
        
        # 确认上下文存在
        contexts_before = sbx.list_code_contexts()
        ids_before = [c.id for c in contexts_before]
        assert context_id in ids_before, "上下文应存在"
        
        # 移除上下文
        sbx.remove_code_context(context)
        print(f"已移除上下文: {context_id}")
        
        # 确认上下文已被移除
        contexts_after = sbx.list_code_contexts()
        ids_after = [c.id for c in contexts_after]
        assert context_id not in ids_after, "上下文应已被移除"
        
        print("✓ 移除上下文测试通过")
        return True
    finally:
        sbx.kill()


def test_restart_context():
    """测试重启上下文 - 清除状态"""
    print("\n" + "=" * 50)
    print("测试: 重启上下文")
    print("=" * 50)
    
    sbx = Sandbox.create()
    try:
        # 创建上下文并定义变量
        context = sbx.create_code_context()
        sbx.run_code("restart_test_var = 'hello'", context=context)
        
        # 验证变量存在
        execution1 = sbx.run_code("print(restart_test_var)", context=context)
        assert "hello" in str(execution1.logs.stdout), "变量应该存在"
        print("变量已定义: restart_test_var = 'hello'")
        
        # 重启上下文
        sbx.restart_code_context(context)
        print("已重启上下文")
        
        # 验证变量不再存在
        execution2 = sbx.run_code("print(restart_test_var)", context=context)
        assert execution2.error is not None, "应该有NameError错误"
        print(f"预期的错误: {execution2.error.name}")
        
        print("✓ 重启上下文测试通过")
        return True
    finally:
        sbx.kill()


def run_all():
    """运行所有上下文管理测试"""
    test_create_code_context()
    test_stateful_execution()
    test_context_cwd()
    test_remove_context()
    test_restart_context()


if __name__ == "__main__":
    run_all()
