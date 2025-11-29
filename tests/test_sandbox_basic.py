"""
基础沙箱测试 - 创建、连接、获取信息
"""
import os
from dotenv import load_dotenv
load_dotenv(override=True)

# 确保环境变量已加载后再导入 e2b
from e2b_code_interpreter import Sandbox


def test_create_sandbox():
    """测试创建沙箱"""
    print("=" * 50)
    print("测试: 创建沙箱")
    print("=" * 50)
    
    sbx = Sandbox.create(template="code-interpreter-v1", timeout=100)
    
    info = sbx.get_info()
    print(f"沙箱 ID: {info.sandbox_id}")
    print(f"模板 ID: {info.template_id}")
    print(f"创建时间: {info.started_at}")
    
    # 列出根目录文件
    files = sbx.files.list("/")
    print(f"根目录文件数: {len(files)}")
    
    sbx.kill()
    print("✓ 沙箱创建测试通过")
    return True


def test_sandbox_list():
    """测试列出所有沙箱"""
    print("\n" + "=" * 50)
    print("测试: 列出沙箱")
    print("=" * 50)
    
    paginator = Sandbox.list()
    sandboxes = paginator.next_items()
    
    print(f"当前运行沙箱数: {len(sandboxes)}")
    for sbx in sandboxes[:5]:  # 只显示前5个
        print(f"  - {sbx.sandbox_id} (模板: {sbx.template_id})")
    
    print("✓ 沙箱列表测试通过")
    return True


def run_all():
    """运行所有基础测试"""
    test_create_sandbox()
    test_sandbox_list()


if __name__ == "__main__":
    run_all()
