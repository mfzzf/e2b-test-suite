"""
pytest 配置和共享 fixtures
"""
import os
import sys
from pathlib import Path
from typing import Generator

import pytest
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

# 导入 SDK
from ucloud_sandbox import Sandbox, AsyncSandbox


@pytest.fixture(scope="session")
def api_key() -> str:
    """获取 API Key"""
    key = os.environ.get("AGENTBOX_API_KEY")
    if not key:
        pytest.skip("AGENTBOX_API_KEY not set")
    return key


@pytest.fixture
def sandbox() -> Generator[Sandbox, None, None]:
    """创建一个沙箱，测试结束后自动销毁"""
    sbx = Sandbox.create(timeout=60)
    yield sbx
    try:
        sbx.kill()
    except Exception:
        pass


@pytest.fixture
def sandbox_with_template() -> Generator[Sandbox, None, None]:
    """使用 base 模板创建沙箱"""
    sbx = Sandbox.create(template="base", timeout=60)
    yield sbx
    try:
        sbx.kill()
    except Exception:
        pass


@pytest.fixture
async def async_sandbox() -> AsyncSandbox:
    """创建异步沙箱"""
    sbx = await AsyncSandbox.create(timeout=60)
    yield sbx
    try:
        await sbx.kill()
    except Exception:
        pass


def pytest_configure(config):
    """pytest 配置钩子"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "beta: marks tests that use beta features"
    )


def run_tests_safely(tests: list, module_name: str = ""):
    """
    安全地运行测试列表，单个测试失败不会终止其他测试
    
    Args:
        tests: 测试函数列表
        module_name: 模块名称（用于打印）
    
    Returns:
        tuple: (passed_tests, failed_tests) - 通过和失败的测试列表
    """
    import traceback
    
    passed = []
    failed = []
    
    for test_func in tests:
        test_name = test_func.__name__
        try:
            test_func()
            passed.append(test_name)
        except Exception as e:
            failed.append((test_name, str(e)))
            print(f"\n❌ 测试 {test_name} 失败: {e}")
            traceback.print_exc()
            print()  # 空行分隔
    
    # 打印总结
    print("\n" + "=" * 60)
    print(f"测试总结{f' ({module_name})' if module_name else ''}")
    print("=" * 60)
    print(f"✅ 通过: {len(passed)}")
    for name in passed:
        print(f"   - {name}")
    print(f"❌ 失败: {len(failed)}")
    for name, error in failed:
        print(f"   - {name}: {error[:50]}...")
    print("=" * 60)
    
    # 如果有失败的测试，抛出异常报告（但所有测试都已运行完）
    if failed:
        raise Exception(f"{len(failed)} 个测试失败: {[name for name, _ in failed]}")
    
    return passed, failed
