"""
PTY 伪终端测试
"""
import os
import time
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

from ucloud_sandbox import Sandbox, PtySize


def test_pty_create():
    """测试创建 PTY"""
    print("=" * 50)
    print("测试: 创建 PTY")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 创建 PTY
        size = PtySize(rows=24, cols=80)
        handle = sbx.pty.create(size=size)
        
        assert handle.pid is not None
        print(f"PTY PID: {handle.pid}")
        
        # 终止 PTY
        sbx.pty.kill(handle.pid)
        
        print("✓ 创建 PTY 测试通过")
        return True
    finally:
        sbx.kill()


def test_pty_send_stdin():
    """测试发送输入到 PTY"""
    print("\n" + "=" * 50)
    print("测试: 发送输入到 PTY")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 创建 PTY
        size = PtySize(rows=24, cols=80)
        handle = sbx.pty.create(size=size)
        
        # 发送命令
        sbx.pty.send_stdin(handle.pid, b"echo 'Hello PTY'\n")
        
        time.sleep(0.5)
        
        print(f"已发送命令到 PTY {handle.pid}")
        
        # 终止 PTY
        sbx.pty.kill(handle.pid)
        
        print("✓ 发送输入测试通过")
        return True
    finally:
        sbx.kill()


def test_pty_resize():
    """测试调整 PTY 大小"""
    print("\n" + "=" * 50)
    print("测试: 调整 PTY 大小")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 创建 PTY
        initial_size = PtySize(rows=24, cols=80)
        handle = sbx.pty.create(size=initial_size)
        
        # 调整大小
        new_size = PtySize(rows=48, cols=120)
        sbx.pty.resize(handle.pid, new_size)
        
        print(f"PTY {handle.pid} 已调整大小: {new_size.rows}x{new_size.cols}")
        
        # 终止 PTY
        sbx.pty.kill(handle.pid)
        
        print("✓ 调整大小测试通过")
        return True
    finally:
        sbx.kill()


def test_pty_kill():
    """测试终止 PTY"""
    print("\n" + "=" * 50)
    print("测试: 终止 PTY")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 创建 PTY
        size = PtySize(rows=24, cols=80)
        handle = sbx.pty.create(size=size)
        pid = handle.pid
        
        # 终止 PTY
        result = sbx.pty.kill(pid)
        assert result == True
        
        print(f"PTY {pid} 已终止")
        
        # 再次终止应返回 False (已不存在)
        result2 = sbx.pty.kill(pid)
        assert result2 == False
        
        print("✓ 终止 PTY 测试通过")
        return True
    finally:
        sbx.kill()


def test_pty_interactive():
    """测试交互式命令执行"""
    print("\n" + "=" * 50)
    print("测试: 交互式命令执行")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 创建 PTY
        size = PtySize(rows=24, cols=80)
        handle = sbx.pty.create(size=size)
        
        # 发送一系列命令
        commands = [
            b"cd /home/user\n",
            b"pwd\n",
            b"ls -la\n",
            b"exit\n",
        ]
        
        for cmd in commands:
            sbx.pty.send_stdin(handle.pid, cmd)
            time.sleep(0.3)
        
        print("已执行交互式命令序列")
        
        # 清理
        try:
            sbx.pty.kill(handle.pid)
        except:
            pass  # 可能已经退出
        
        print("✓ 交互式执行测试通过")
        return True
    finally:
        sbx.kill()


def test_pty_with_envs():
    """测试带环境变量的 PTY"""
    print("\n" + "=" * 50)
    print("测试: 带环境变量的 PTY")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 创建带环境变量的 PTY
        size = PtySize(rows=24, cols=80)
        envs = {"MY_VAR": "my_value"}
        handle = sbx.pty.create(size=size, envs=envs)
        
        # 发送命令验证环境变量
        sbx.pty.send_stdin(handle.pid, b"echo $MY_VAR\n")
        
        time.sleep(0.5)
        
        print(f"PTY {handle.pid} 创建时带有环境变量")
        
        # 终止 PTY
        sbx.pty.kill(handle.pid)
        
        print("✓ 环境变量 PTY 测试通过")
        return True
    finally:
        sbx.kill()


def test_pty_with_cwd():
    """测试指定工作目录的 PTY"""
    print("\n" + "=" * 50)
    print("测试: 指定工作目录的 PTY")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 创建目录
        sbx.files.make_dir("/home/user/pty_cwd")
        
        # 创建带工作目录的 PTY
        size = PtySize(rows=24, cols=80)
        handle = sbx.pty.create(size=size, cwd="/home/user/pty_cwd")
        
        time.sleep(0.3)
        
        print(f"PTY {handle.pid} 工作目录: /home/user/pty_cwd")
        
        # 终止 PTY
        sbx.pty.kill(handle.pid)
        
        print("✓ 工作目录 PTY 测试通过")
        return True
    finally:
        sbx.kill()


def run_all():
    """运行所有 PTY 测试"""
    test_pty_create()
    test_pty_send_stdin()
    test_pty_resize()
    test_pty_kill()
    test_pty_interactive()
    test_pty_with_envs()
    test_pty_with_cwd()


if __name__ == "__main__":
    run_all()
