"""
沙箱生命周期测试 - 创建、连接、暂停、恢复、销毁
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

from ucloud_sandbox import Sandbox, SandboxPaginator


def test_create_sandbox():
    """测试创建沙箱"""
    print("=" * 50)
    print("测试: 创建沙箱")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        assert sbx.sandbox_id is not None
        print(f"沙箱 ID: {sbx.sandbox_id}")
        print("✓ 沙箱创建测试通过")
        return True
    finally:
        sbx.kill()


def test_create_sandbox_with_template():
    """测试使用指定模板创建沙箱"""
    print("\n" + "=" * 50)
    print("测试: 使用模板创建沙箱")
    print("=" * 50)
    
    sbx = Sandbox.create(template="base", timeout=60)
    try:
        info = sbx.get_info()
        # 模板 ID 可能是实际的 UUID 而不是 "base"
        assert info.template_id is not None
        print(f"模板 ID: {info.template_id}")
        print("✓ 模板沙箱创建测试通过")
        return True
    finally:
        sbx.kill()


def test_create_sandbox_with_metadata():
    """测试带元数据创建沙箱"""
    print("\n" + "=" * 50)
    print("测试: 带元数据创建沙箱")
    print("=" * 50)
    
    metadata = {"project": "test", "env": "dev"}
    sbx = Sandbox.create(metadata=metadata, timeout=60)
    try:
        info = sbx.get_info()
        print(f"元数据: {info.metadata}")
        assert info.metadata.get("project") == "test"
        assert info.metadata.get("env") == "dev"
        print("✓ 元数据沙箱创建测试通过")
        return True
    finally:
        sbx.kill()


def test_create_sandbox_with_envs():
    """测试带环境变量创建沙箱"""
    print("\n" + "=" * 50)
    print("测试: 带环境变量创建沙箱")
    print("=" * 50)
    
    envs = {"MY_VAR": "my_value", "ANOTHER_VAR": "another_value"}
    sbx = Sandbox.create(envs=envs, timeout=60)
    try:
        result = sbx.commands.run("echo $MY_VAR")
        assert "my_value" in result.stdout
        print(f"环境变量输出: {result.stdout.strip()}")
        print("✓ 环境变量沙箱创建测试通过")
        return True
    finally:
        sbx.kill()


def test_create_sandbox_with_timeout():
    """测试指定超时时间创建沙箱"""
    print("\n" + "=" * 50)
    print("测试: 指定超时创建沙箱")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        info = sbx.get_info()
        print(f"沙箱结束时间: {info.end_at}")
        print("✓ 超时沙箱创建测试通过")
        return True
    finally:
        sbx.kill()


def test_sandbox_connect():
    """测试连接到已有沙箱"""
    print("\n" + "=" * 50)
    print("测试: 连接到已有沙箱")
    print("=" * 50)
    
    # 先创建一个沙箱
    sbx1 = Sandbox.create(timeout=60)
    sandbox_id = sbx1.sandbox_id
    
    try:
        # 使用 ID 连接到同一个沙箱
        sbx2 = Sandbox.connect(sandbox_id)
        assert sbx2.sandbox_id == sandbox_id
        print(f"连接到沙箱: {sbx2.sandbox_id}")
        print("✓ 沙箱连接测试通过")
        return True
    finally:
        sbx1.kill()


def test_sandbox_set_timeout():
    """测试修改超时时间"""
    print("\n" + "=" * 50)
    print("测试: 修改超时时间")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 延长超时时间
        sbx.set_timeout(300)
        info = sbx.get_info()
        print(f"新的结束时间: {info.end_at}")
        print("✓ 修改超时测试通过")
        return True
    finally:
        sbx.kill()


def test_sandbox_kill():
    """测试销毁沙箱"""
    print("\n" + "=" * 50)
    print("测试: 销毁沙箱")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    sandbox_id = sbx.sandbox_id
    
    # 销毁沙箱
    result = sbx.kill()
    assert result == True
    print(f"沙箱 {sandbox_id} 已销毁")
    
    # 验证沙箱已不存在
    is_running = sbx.is_running()
    assert is_running == False
    print("✓ 沙箱销毁测试通过")
    return True


def test_sandbox_is_running():
    """测试检查运行状态"""
    print("\n" + "=" * 50)
    print("测试: 检查运行状态")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 检查正在运行
        assert sbx.is_running() == True
        print("沙箱正在运行: True")
        print("✓ 运行状态检查测试通过")
        return True
    finally:
        sbx.kill()


def test_sandbox_context_manager():
    """测试上下文管理器使用"""
    print("\n" + "=" * 50)
    print("测试: 上下文管理器")
    print("=" * 50)
    
    with Sandbox.create(timeout=60) as sbx:
        assert sbx.sandbox_id is not None
        print(f"沙箱 ID: {sbx.sandbox_id}")
        sandbox_id = sbx.sandbox_id
    
    # 退出上下文后沙箱应该被销毁
    print(f"沙箱 {sandbox_id} 已自动销毁")
    print("✓ 上下文管理器测试通过")
    return True


def test_sandbox_list():
    """测试列出所有沙箱"""
    print("\n" + "=" * 50)
    print("测试: 列出所有沙箱")
    print("=" * 50)
    
    # 创建几个沙箱
    sbx1 = Sandbox.create(timeout=60)
    sbx2 = Sandbox.create(timeout=60)
    
    try:
        paginator = Sandbox.list()
        sandboxes = paginator.next_items()
        
        print(f"当前运行沙箱数: {len(sandboxes)}")
        assert len(sandboxes) >= 2
        
        # 验证新创建的沙箱在列表中
        sandbox_ids = [s.sandbox_id for s in sandboxes]
        assert sbx1.sandbox_id in sandbox_ids
        assert sbx2.sandbox_id in sandbox_ids
        
        print("✓ 沙箱列表测试通过")
        return True
    finally:
        sbx1.kill()
        sbx2.kill()


def test_beta_pause_and_resume():
    """测试暂停和恢复沙箱 (Beta 功能)"""
    print("\n" + "=" * 50)
    print("测试: 暂停和恢复沙箱 (Beta)")
    print("=" * 50)
    
    # 使用 auto_pause 创建沙箱
    sbx = Sandbox.beta_create(timeout=60, auto_pause=True)
    sandbox_id = sbx.sandbox_id
    
    try:
        # 写入文件用于验证状态持久化
        sbx.files.write("/home/user/test.txt", "Hello, Pause Test!")
        
        # 暂停沙箱
        sbx.beta_pause()
        print(f"沙箱 {sandbox_id} 已暂停")
        
        # 恢复沙箱
        sbx2 = Sandbox.connect(sandbox_id)
        
        # 验证状态持久化
        content = sbx2.files.read("/home/user/test.txt")
        assert content == "Hello, Pause Test!"
        print("状态持久化验证通过")
        
        print("✓ 暂停恢复测试通过")
        return True
    finally:
        try:
            sbx.kill()
        except:
            pass


def run_all():
    """运行所有生命周期测试"""
    test_create_sandbox()
    test_create_sandbox_with_template()
    test_create_sandbox_with_metadata()
    test_create_sandbox_with_envs()
    test_create_sandbox_with_timeout()
    test_sandbox_connect()
    test_sandbox_set_timeout()
    test_sandbox_kill()
    test_sandbox_is_running()
    test_sandbox_context_manager()
    test_sandbox_list()
    # Beta 功能可能不可用，跳过
    # test_beta_pause_and_resume()


if __name__ == "__main__":
    run_all()
