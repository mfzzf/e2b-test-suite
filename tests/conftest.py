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
from ucloud_agentbox import Sandbox, AsyncSandbox


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
    sbx = Sandbox.create(timeout=300)
    yield sbx
    try:
        sbx.kill()
    except Exception:
        pass


@pytest.fixture
def sandbox_with_template() -> Generator[Sandbox, None, None]:
    """使用 base 模板创建沙箱"""
    sbx = Sandbox.create(template="base", timeout=300)
    yield sbx
    try:
        sbx.kill()
    except Exception:
        pass


@pytest.fixture
async def async_sandbox() -> AsyncSandbox:
    """创建异步沙箱"""
    sbx = await AsyncSandbox.create(timeout=300)
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
