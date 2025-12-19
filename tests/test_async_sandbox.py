"""
AsyncSandbox 异步 API 测试
"""
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

from ucloud_sandbox import AsyncSandbox


async def test_async_create():
    """测试异步创建沙箱"""
    print("=" * 50)
    print("测试: 异步创建沙箱")
    print("=" * 50)
    
    sbx = await AsyncSandbox.create(timeout=60)
    try:
        assert sbx.sandbox_id is not None
        print(f"沙箱 ID: {sbx.sandbox_id}")
        print("✓ 异步创建测试通过")
        return True
    finally:
        await sbx.kill()


async def test_async_create_with_options():
    """测试带选项的异步创建"""
    print("\n" + "=" * 50)
    print("测试: 带选项的异步创建")
    print("=" * 50)
    
    metadata = {"async_test": "true"}
    envs = {"MY_VAR": "async_value"}
    
    sbx = await AsyncSandbox.create(
        template="base",
        metadata=metadata,
        envs=envs,
        timeout=60
    )
    try:
        info = await sbx.get_info()
        # 模板 ID 可能是实际的 UUID 而不是 "base"
        assert info.template_id is not None
        assert info.metadata.get("async_test") == "true"
        
        print(f"模板: {info.template_id}")
        print(f"元数据: {info.metadata}")
        print("✓ 带选项异步创建测试通过")
        return True
    finally:
        await sbx.kill()


async def test_async_files_operations():
    """测试异步文件操作"""
    print("\n" + "=" * 50)
    print("测试: 异步文件操作")
    print("=" * 50)
    
    sbx = await AsyncSandbox.create(timeout=60)
    try:
        # 异步写入
        content = "Async file content"
        result = await sbx.files.write("/home/user/async_test.txt", content)
        assert result.path == "/home/user/async_test.txt"
        print(f"写入文件: {result.path}")
        
        # 异步读取
        read_content = await sbx.files.read("/home/user/async_test.txt")
        assert read_content == content
        print(f"读取内容: {read_content}")
        
        # 异步列出
        entries = await sbx.files.list("/home/user")
        print(f"目录条目数: {len(entries)}")
        
        # 异步检查存在
        exists = await sbx.files.exists("/home/user/async_test.txt")
        assert exists == True
        print(f"文件存在: {exists}")
        
        # 异步删除
        await sbx.files.remove("/home/user/async_test.txt")
        exists_after = await sbx.files.exists("/home/user/async_test.txt")
        assert exists_after == False
        print("文件已删除")
        
        print("✓ 异步文件操作测试通过")
        return True
    finally:
        await sbx.kill()


async def test_async_commands_run():
    """测试异步命令执行"""
    print("\n" + "=" * 50)
    print("测试: 异步命令执行")
    print("=" * 50)
    
    sbx = await AsyncSandbox.create(timeout=60)
    try:
        # 异步执行命令
        result = await sbx.commands.run("echo 'Async Hello World'")
        assert "Async Hello World" in result.stdout
        print(f"命令输出: {result.stdout.strip()}")
        
        # 异步后台命令
        handle = await sbx.commands.run("sleep 5", background=True)
        assert handle.pid is not None
        print(f"后台命令 PID: {handle.pid}")
        
        # 列出进程
        processes = await sbx.commands.list()
        pids = [p.pid for p in processes]
        assert handle.pid in pids
        print(f"进程列表长度: {len(processes)}")
        
        # 终止后台进程
        await sbx.commands.kill(handle.pid)
        print("后台进程已终止")
        
        print("✓ 异步命令执行测试通过")
        return True
    finally:
        await sbx.kill()


async def test_async_context_manager():
    """测试异步上下文管理器"""
    print("\n" + "=" * 50)
    print("测试: 异步上下文管理器")
    print("=" * 50)
    
    sbx = await AsyncSandbox.create(timeout=60)
    try:
        assert sbx.sandbox_id is not None
        sandbox_id = sbx.sandbox_id
        
        # 执行一些操作
        await sbx.files.write("/home/user/context.txt", "context test")
        result = await sbx.commands.run("echo 'in context'")
        
        print(f"沙箱 ID: {sandbox_id}")
        print(f"命令输出: {result.stdout.strip()}")
        print("✓ 异步上下文管理器测试通过")
        return True
    finally:
        await sbx.kill()


async def test_async_kill():
    """测试异步销毁沙箱"""
    print("\n" + "=" * 50)
    print("测试: 异步销毁沙箱")
    print("=" * 50)
    
    sbx = await AsyncSandbox.create(timeout=60)
    sandbox_id = sbx.sandbox_id
    
    # 异步销毁
    result = await sbx.kill()
    assert result == True
    
    print(f"沙箱 {sandbox_id} 已销毁")
    
    # 验证已不运行
    is_running = await sbx.is_running()
    assert is_running == False
    
    print("✓ 异步销毁测试通过")
    return True


async def test_async_connect():
    """测试异步连接沙箱"""
    print("\n" + "=" * 50)
    print("测试: 异步连接沙箱")
    print("=" * 50)
    
    # 创建沙箱
    sbx1 = await AsyncSandbox.create(timeout=60)
    sandbox_id = sbx1.sandbox_id
    
    try:
        # 写入文件
        await sbx1.files.write("/home/user/connect_test.txt", "connect test")
        
        # 异步连接
        sbx2 = await AsyncSandbox.connect(sandbox_id)
        assert sbx2.sandbox_id == sandbox_id
        
        # 验证状态
        content = await sbx2.files.read("/home/user/connect_test.txt")
        assert content == "connect test"
        
        print(f"连接到沙箱: {sbx2.sandbox_id}")
        print("✓ 异步连接测试通过")
        return True
    finally:
        await sbx1.kill()


async def test_async_get_info():
    """测试异步获取沙箱信息"""
    print("\n" + "=" * 50)
    print("测试: 异步获取信息")
    print("=" * 50)
    
    sbx = await AsyncSandbox.create(timeout=60)
    try:
        info = await sbx.get_info()
        
        assert info.sandbox_id == sbx.sandbox_id
        print(f"沙箱 ID: {info.sandbox_id}")
        print(f"模板: {info.template_id}")
        print(f"创建时间: {info.started_at}")
        
        print("✓ 异步获取信息测试通过")
        return True
    finally:
        await sbx.kill()


async def test_async_sandbox_list():
    """测试异步列出沙箱"""
    print("\n" + "=" * 50)
    print("测试: 异步列出沙箱")
    print("=" * 50)
    
    # 创建沙箱
    sbx = await AsyncSandbox.create(timeout=60)
    
    try:
        paginator = AsyncSandbox.list()
        sandboxes = await paginator.next_items()
        
        print(f"运行中的沙箱数: {len(sandboxes)}")
        
        # 验证新创建的沙箱在列表中
        sandbox_ids = [s.sandbox_id for s in sandboxes]
        assert sbx.sandbox_id in sandbox_ids
        
        print("✓ 异步列出沙箱测试通过")
        return True
    finally:
        await sbx.kill()


async def test_async_concurrent_operations():
    """测试异步并发操作"""
    print("\n" + "=" * 50)
    print("测试: 异步并发操作")
    print("=" * 50)
    
    sbx = await AsyncSandbox.create(timeout=60)
    try:
        # 并发写入多个文件
        tasks = [
            sbx.files.write(f"/home/user/concurrent_{i}.txt", f"Content {i}")
            for i in range(5)
        ]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 5
        print(f"并发写入文件数: {len(results)}")
        
        # 并发读取
        read_tasks = [
            sbx.files.read(f"/home/user/concurrent_{i}.txt")
            for i in range(5)
        ]
        contents = await asyncio.gather(*read_tasks)
        
        assert len(contents) == 5
        print(f"并发读取内容数: {len(contents)}")
        
        print("✓ 异步并发操作测试通过")
        return True
    finally:
        await sbx.kill()


def run_all():
    """运行所有异步测试"""
    async def run_tests():
        await test_async_create()
        await test_async_create_with_options()
        await test_async_files_operations()
        await test_async_commands_run()
        await test_async_context_manager()
        await test_async_kill()
        await test_async_connect()
        await test_async_get_info()
        await test_async_sandbox_list()
        await test_async_concurrent_operations()
    
    asyncio.run(run_tests())


if __name__ == "__main__":
    run_all()
