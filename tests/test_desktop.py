"""
桌面沙箱测试 - VNC 流、应用启动
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)
from e2b_desktop import Sandbox


def test_desktop_create():
    """测试创建桌面沙箱"""
    print("=" * 50)
    print("测试: 创建桌面沙箱")
    print("=" * 50)
    
    desktop = Sandbox.create(template="desktop", timeout=300)
    try:
        print(f"桌面沙箱已创建")
        
        # 等待桌面启动
        desktop.wait(5000)
        
        # 启动流
        desktop.stream.start(require_auth=True)
        auth_key = desktop.stream.get_auth_key()
        stream_url = desktop.stream.get_url(auth_key=auth_key)
        
        print(f"流地址: {stream_url}")
        
        print("✓ 桌面沙箱创建测试通过")
        return True
    finally:
        desktop.kill()


def test_desktop_file_operations():
    """测试桌面沙箱文件操作"""
    print("\n" + "=" * 50)
    print("测试: 桌面沙箱文件操作")
    print("=" * 50)
    
    desktop = Sandbox.create(template="desktop", timeout=300)
    try:
        # 写入文件
        desktop.files.write("/home/user/test.js", "console.log('hello from desktop')")
        print("✓ 文件写入成功")
        
        # 打开文件
        desktop.open("/home/user/test.js")
        print("✓ 文件打开成功")
        
        desktop.wait(2000)
        
        print("✓ 桌面文件操作测试通过")
        return True
    finally:
        desktop.kill()


def test_desktop_stream():
    """测试桌面流"""
    print("\n" + "=" * 50)
    print("测试: 桌面流")
    print("=" * 50)
    
    desktop = Sandbox.create(template="desktop", timeout=300)
    try:
        desktop.wait(3000)
        
        # 启动流
        desktop.stream.start(require_auth=True)
        auth_key = desktop.stream.get_auth_key()
        stream_url = desktop.stream.get_url(auth_key=auth_key)
        
        print(f"认证密钥: {auth_key[:20]}...")
        print(f"流地址: {stream_url}")
        
        print("✓ 桌面流测试通过")
        return True
    finally:
        desktop.kill()


def run_all():
    """运行所有桌面测试"""
    test_desktop_create()
    test_desktop_file_operations()
    test_desktop_stream()


if __name__ == "__main__":
    run_all()
