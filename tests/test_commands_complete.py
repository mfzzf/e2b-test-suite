"""
命令执行完整测试
"""
import os
import time
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

from ucloud_sandbox import Sandbox, CommandResult, ProcessInfo
from ucloud_sandbox.sandbox.commands.command_handle import CommandExitException


def test_run_simple_command():
    """测试执行简单命令"""
    print("=" * 50)
    print("测试: 执行简单命令")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        result = sbx.commands.run("echo 'Hello World'")
        
        assert "Hello World" in result.stdout
        print(f"命令输出: {result.stdout.strip()}")
        print(f"退出码: {result.exit_code}")
        print("✓ 简单命令执行测试通过")
        return True
    finally:
        sbx.kill()


def test_run_command_with_output():
    """测试获取命令输出"""
    print("\n" + "=" * 50)
    print("测试: 获取命令输出")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 测试 stdout
        result = sbx.commands.run("ls -la /home/user")
        assert len(result.stdout) > 0
        print(f"stdout 长度: {len(result.stdout)}")
        
        # 测试 stderr
        result2 = sbx.commands.run("ls /nonexistent 2>&1 || true")
        print(f"命令输出: {result2.stdout}")
        
        print("✓ 命令输出测试通过")
        return True
    finally:
        sbx.kill()


def test_run_command_with_envs():
    """测试使用环境变量"""
    print("\n" + "=" * 50)
    print("测试: 使用环境变量")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        env_vars = {"MY_VAR": "my_value", "ANOTHER": "123"}
        result = sbx.commands.run(
            "echo $MY_VAR-$ANOTHER",
            envs=env_vars
        )
        
        assert "my_value-123" in result.stdout
        print(f"环境变量输出: {result.stdout.strip()}")
        print("✓ 环境变量测试通过")
        return True
    finally:
        sbx.kill()


def test_run_command_with_cwd():
    """测试指定工作目录"""
    print("\n" + "=" * 50)
    print("测试: 指定工作目录")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 创建测试目录
        sbx.files.make_dir("/home/user/test_cwd")
        
        result = sbx.commands.run("pwd", cwd="/home/user/test_cwd")
        
        assert "/home/user/test_cwd" in result.stdout
        print(f"工作目录: {result.stdout.strip()}")
        print("✓ 工作目录测试通过")
        return True
    finally:
        sbx.kill()


def test_run_command_with_user():
    """测试指定用户执行"""
    print("\n" + "=" * 50)
    print("测试: 指定用户执行")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        result = sbx.commands.run("whoami", user="user")
        
        assert "user" in result.stdout
        print(f"当前用户: {result.stdout.strip()}")
        print("✓ 指定用户测试通过")
        return True
    finally:
        sbx.kill()


def test_run_background_command():
    """测试后台执行命令"""
    print("\n" + "=" * 50)
    print("测试: 后台执行命令")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 启动后台命令
        handle = sbx.commands.run("sleep 5 && echo 'done'", background=True)
        
        assert handle.pid is not None
        print(f"后台进程 PID: {handle.pid}")
        
        # 不等待完成，直接检查进程列表
        processes = sbx.commands.list()
        pids = [p.pid for p in processes]
        assert handle.pid in pids
        
        # 终止后台进程
        sbx.commands.kill(handle.pid)
        
        print("✓ 后台命令测试通过")
        return True
    finally:
        sbx.kill()


def test_command_with_callbacks():
    """测试输出回调处理"""
    print("\n" + "=" * 50)
    print("测试: 输出回调处理")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        stdout_lines = []
        stderr_lines = []
        
        def on_stdout(line):
            stdout_lines.append(line)
            print(f"stdout: {line.strip()}")
        
        def on_stderr(line):
            stderr_lines.append(line)
            print(f"stderr: {line.strip()}")
        
        result = sbx.commands.run(
            "echo 'line1'; echo 'line2'; echo 'error' >&2",
            on_stdout=on_stdout,
            on_stderr=on_stderr
        )
        
        print(f"收到 stdout 行数: {len(stdout_lines)}")
        print(f"收到 stderr 行数: {len(stderr_lines)}")
        print("✓ 输出回调测试通过")
        return True
    finally:
        sbx.kill()


def test_command_send_stdin():
    """测试发送标准输入"""
    print("\n" + "=" * 50)
    print("测试: 发送标准输入")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 启动交互式命令
        handle = sbx.commands.run("cat", background=True, stdin=True)
        
        # 发送输入
        sbx.commands.send_stdin(handle.pid, "Hello from stdin\n")
        
        time.sleep(0.5)
        
        # 终止
        sbx.commands.kill(handle.pid)
        
        print("✓ 发送标准输入测试通过")
        return True
    finally:
        sbx.kill()


def test_command_kill():
    """测试终止命令"""
    print("\n" + "=" * 50)
    print("测试: 终止命令")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 启动长时间运行的命令
        handle = sbx.commands.run("sleep 60", background=True)
        pid = handle.pid
        
        # 验证进程存在
        processes = sbx.commands.list()
        pids = [p.pid for p in processes]
        assert pid in pids
        
        # 终止命令
        result = sbx.commands.kill(pid)
        assert result == True
        
        # 验证进程已终止
        time.sleep(0.5)
        processes = sbx.commands.list()
        pids = [p.pid for p in processes]
        assert pid not in pids
        
        print(f"进程 {pid} 已终止")
        print("✓ 终止命令测试通过")
        return True
    finally:
        sbx.kill()


def test_commands_list():
    """测试列出运行中的命令"""
    print("\n" + "=" * 50)
    print("测试: 列出运行中的命令")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 启动几个后台命令
        h1 = sbx.commands.run("sleep 30", background=True)
        h2 = sbx.commands.run("sleep 30", background=True)
        
        # 列出进程
        processes = sbx.commands.list()
        
        print(f"运行中的进程数: {len(processes)}")
        for p in processes:
            print(f"  - PID: {p.pid}, CMD: {p.cmd}")
        
        # 验证新启动的进程在列表中
        pids = [p.pid for p in processes]
        assert h1.pid in pids
        assert h2.pid in pids
        
        # 清理
        sbx.commands.kill(h1.pid)
        sbx.commands.kill(h2.pid)
        
        print("✓ 列出命令测试通过")
        return True
    finally:
        sbx.kill()


def test_command_connect():
    """测试连接到运行中的命令"""
    print("\n" + "=" * 50)
    print("测试: 连接到运行中的命令")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 启动后台命令
        handle = sbx.commands.run("sleep 10", background=True)
        pid = handle.pid
        
        # 连接到该命令
        connected_handle = sbx.commands.connect(pid)
        
        assert connected_handle.pid == pid
        print(f"连接到进程: {connected_handle.pid}")
        
        # 清理
        sbx.commands.kill(pid)
        
        print("✓ 连接命令测试通过")
        return True
    finally:
        sbx.kill()


def test_command_timeout():
    """测试命令超时处理"""
    print("\n" + "=" * 50)
    print("测试: 命令超时处理")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 执行快速命令，设置短超时
        result = sbx.commands.run("echo 'fast'", timeout=10)
        assert "fast" in result.stdout
        print("快速命令完成")
        
        # 后台命令不会超时阻塞
        handle = sbx.commands.run("sleep 100", background=True, timeout=5)
        assert handle.pid is not None
        
        # 清理
        sbx.commands.kill(handle.pid)
        
        print("✓ 命令超时测试通过")
        return True
    finally:
        sbx.kill()


def test_command_error():
    """测试命令错误处理"""
    print("\n" + "=" * 50)
    print("测试: 命令错误处理")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 执行会失败的命令 - SDK 会抛出 CommandExitException
        try:
            result = sbx.commands.run("exit 1")
            # 如果没有抛出异常，检查退出码
            assert result.exit_code == 1
            print(f"退出码: {result.exit_code}")
        except CommandExitException as e:
            print(f"正确捕获 CommandExitException: 退出码 {e.exit_code}")
        
        # 执行不存在的命令
        result2 = sbx.commands.run("nonexistent_command 2>&1 || true")
        print(f"命令输出: {result2.stdout}")
        
        print("✓ 命令错误处理测试通过")
        return True
    finally:
        sbx.kill()


def test_command_multiline():
    """测试多行命令"""
    print("\n" + "=" * 50)
    print("测试: 多行命令")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        cmd = """
echo "Line 1"
echo "Line 2"
echo "Line 3"
"""
        result = sbx.commands.run(cmd)
        
        assert "Line 1" in result.stdout
        assert "Line 2" in result.stdout
        assert "Line 3" in result.stdout
        
        print(f"多行命令输出:\n{result.stdout}")
        print("✓ 多行命令测试通过")
        return True
    finally:
        sbx.kill()


def test_command_with_args():
    """测试带参数的命令"""
    print("\n" + "=" * 50)
    print("测试: 带参数的命令")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=60)
    try:
        # 使用引号和特殊字符
        result = sbx.commands.run("echo 'Hello \"World\"'")
        print(f"输出: {result.stdout.strip()}")
        
        # 使用管道
        result2 = sbx.commands.run("echo 'abc' | tr 'a-z' 'A-Z'")
        assert "ABC" in result2.stdout
        print(f"管道输出: {result2.stdout.strip()}")
        
        print("✓ 带参数命令测试通过")
        return True
    finally:
        sbx.kill()


def run_all():
    """运行所有命令执行测试"""
    test_run_simple_command()
    test_run_command_with_output()
    test_run_command_with_envs()
    test_run_command_with_cwd()
    test_run_command_with_user()
    test_run_background_command()
    test_command_with_callbacks()
    test_command_send_stdin()
    test_command_kill()
    test_commands_list()
    test_command_connect()
    test_command_timeout()
    test_command_error()
    test_command_multiline()
    test_command_with_args()


if __name__ == "__main__":
    run_all()
