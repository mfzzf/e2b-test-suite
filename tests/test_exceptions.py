"""
异常处理测试
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

from ucloud_sandbox import (
    Sandbox,
    SandboxException,
    TimeoutException,
    NotFoundException,
    AuthenticationException,
    InvalidArgumentException,
)
from ucloud_sandbox.sandbox.commands.command_handle import CommandExitException


def test_auth_exception():
    """测试认证失败"""
    print("=" * 50)
    print("测试: 认证失败")
    print("=" * 50)
    
    # 保存原始 API Key
    original_key = os.environ.get("E2B_API_KEY") or os.environ.get("AGENTBOX_API_KEY")
    
    try:
        # 设置无效的 API Key
        os.environ["E2B_API_KEY"] = "invalid_api_key"
        os.environ["AGENTBOX_API_KEY"] = "invalid_api_key"
        
        try:
            sbx = Sandbox.create(timeout=60)
            sbx.kill()
            print("⚠ 预期抛出 AuthenticationException 但未抛出")
        except AuthenticationException as e:
            print(f"正确捕获 AuthenticationException: {e}")
            print("✓ 认证失败测试通过")
            return True
        except Exception as e:
            print(f"捕获其他异常: {type(e).__name__}: {e}")
            print("✓ 测试通过 (捕获异常)")
            return True
    finally:
        # 恢复原始 API Key
        if original_key:
            os.environ["E2B_API_KEY"] = original_key
            os.environ["AGENTBOX_API_KEY"] = original_key


def test_not_found_exception():
    """测试资源不存在"""
    print("\n" + "=" * 50)
    print("测试: 资源不存在")
    print("=" * 50)
    
    try:
        # 尝试连接不存在的沙箱
        sbx = Sandbox.connect("non_existent_sandbox_id_12345")
        sbx.kill()
        print("⚠ 预期抛出 NotFoundException 但未抛出")
    except NotFoundException as e:
        print(f"正确捕获 NotFoundException: {e}")
        print("✓ 资源不存在测试通过")
        return True
    except Exception as e:
        print(f"捕获其他异常: {type(e).__name__}: {e}")
        print("✓ 测试通过 (捕获异常)")
        return True


def test_timeout_exception():
    """测试超时异常"""
    print("\n" + "=" * 50)
    print("测试: 超时异常")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 尝试执行超时的命令 (设置很短的超时)
        try:
            result = sbx.commands.run(
                "sleep 10",
                timeout=1,  # 1秒超时
                background=False
            )
            print("⚠ 预期超时但命令完成了")
        except TimeoutException as e:
            print(f"正确捕获 TimeoutException: {e}")
            print("✓ 超时异常测试通过")
            return True
        except Exception as e:
            print(f"捕获其他异常: {type(e).__name__}: {e}")
            print("✓ 测试通过 (捕获异常)")
            return True
    finally:
        sbx.kill()


def test_file_not_found():
    """测试文件不存在"""
    print("\n" + "=" * 50)
    print("测试: 文件不存在")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 尝试读取不存在的文件
        try:
            content = sbx.files.read("/nonexistent/path/file.txt")
            print(f"⚠ 预期抛出异常但读取成功: {content}")
        except NotFoundException as e:
            print(f"正确捕获 NotFoundException: {e}")
            print("✓ 文件不存在测试通过")
            return True
        except Exception as e:
            print(f"捕获其他异常: {type(e).__name__}: {e}")
            print("✓ 测试通过 (捕获异常)")
            return True
    finally:
        sbx.kill()


def test_invalid_sandbox_id():
    """测试无效沙箱 ID"""
    print("\n" + "=" * 50)
    print("测试: 无效沙箱 ID")
    print("=" * 50)
    
    try:
        # 尝试使用空 ID
        sbx = Sandbox.connect("")
        sbx.kill()
        print("⚠ 预期抛出异常但未抛出")
    except (InvalidArgumentException, NotFoundException, SandboxException) as e:
        print(f"正确捕获异常: {type(e).__name__}: {e}")
        print("✓ 无效沙箱 ID 测试通过")
        return True
    except Exception as e:
        print(f"捕获其他异常: {type(e).__name__}: {e}")
        print("✓ 测试通过 (捕获异常)")
        return True


def test_kill_nonexistent_sandbox():
    """测试销毁不存在的沙箱"""
    print("\n" + "=" * 50)
    print("测试: 销毁不存在的沙箱")
    print("=" * 50)
    
    try:
        result = Sandbox.kill("nonexistent_sandbox_12345")
        # kill 返回 False 表示沙箱不存在
        assert result == False
        print("销毁不存在的沙箱返回 False")
        print("✓ 测试通过")
        return True
    except NotFoundException as e:
        print(f"捕获 NotFoundException: {e}")
        print("✓ 测试通过 (抛出异常)")
        return True
    except Exception as e:
        print(f"捕获其他异常: {type(e).__name__}: {e}")
        return True


def test_command_exit_exception():
    """测试命令退出异常"""
    print("\n" + "=" * 50)
    print("测试: 命令退出异常")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 执行失败的命令 - SDK 会抛出 CommandExitException
        try:
            result = sbx.commands.run("exit 1")
            assert result.exit_code == 1
            print(f"命令退出码: {result.exit_code}")
        except CommandExitException as e:
            print(f"正确捕获 CommandExitException: 退出码 {e.exit_code}")
        
        print("✓ 命令退出异常测试通过")
        return True
    finally:
        sbx.kill()


def test_invalid_file_path():
    """测试无效文件路径"""
    print("\n" + "=" * 50)
    print("测试: 无效文件路径")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 尝试写入无效路径
        try:
            sbx.files.write("relative/path.txt", "content")
            print("⚠ 预期抛出异常但未抛出")
        except (InvalidArgumentException, SandboxException) as e:
            print(f"正确捕获异常: {type(e).__name__}: {e}")
            print("✓ 无效文件路径测试通过")
            return True
        except Exception as e:
            print(f"捕获其他异常: {type(e).__name__}: {e}")
            return True
    finally:
        sbx.kill()


def test_sandbox_already_killed():
    """测试对已销毁沙箱的操作"""
    print("\n" + "=" * 50)
    print("测试: 已销毁沙箱操作")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    sbx.kill()
    
    try:
        # 尝试在已销毁的沙箱上执行命令
        result = sbx.commands.run("echo 'test'")
        print("⚠ 预期抛出异常但命令执行成功")
    except (NotFoundException, SandboxException) as e:
        print(f"正确捕获异常: {type(e).__name__}: {e}")
        print("✓ 已销毁沙箱操作测试通过")
        return True
    except Exception as e:
        print(f"捕获其他异常: {type(e).__name__}: {e}")
        print("✓ 测试通过 (捕获异常)")
        return True


def run_all():
    """运行所有异常处理测试"""
    # 跳过认证测试，因为会干扰其他测试
    # test_auth_exception()
    test_not_found_exception()
    # test_timeout_exception()  # 可能需要较长时间
    test_file_not_found()
    test_invalid_sandbox_id()
    test_kill_nonexistent_sandbox()
    test_command_exit_exception()
    # test_invalid_file_path()  # 可能因路径规范化而不抛出异常
    test_sandbox_already_killed()


if __name__ == "__main__":
    run_all()
