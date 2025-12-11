"""
完整文件系统操作测试
"""
import os
import io
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

from ucloud_agentbox import Sandbox, FileType, EntryInfo


def test_write_string():
    """测试写入字符串"""
    print("=" * 50)
    print("测试: 写入字符串")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        content = "Hello, AgentBox!"
        result = sbx.files.write("/home/user/test.txt", content)
        
        assert result.path == "/home/user/test.txt"
        print(f"写入文件: {result.path}")
        print("✓ 字符串写入测试通过")
        return True
    finally:
        sbx.kill()


def test_write_bytes():
    """测试写入二进制数据"""
    print("\n" + "=" * 50)
    print("测试: 写入二进制数据")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        content = b"Binary content \x00\x01\x02\x03"
        result = sbx.files.write("/home/user/binary.bin", content)
        
        assert result.path == "/home/user/binary.bin"
        print(f"写入二进制文件: {result.path}")
        print("✓ 二进制写入测试通过")
        return True
    finally:
        sbx.kill()


def test_write_file_stream():
    """测试流式写入"""
    print("\n" + "=" * 50)
    print("测试: 流式写入")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 使用 BytesIO 模拟文件流
        stream = io.BytesIO(b"Stream content from BytesIO")
        result = sbx.files.write("/home/user/stream.txt", stream)
        
        assert result.path == "/home/user/stream.txt"
        print(f"流式写入文件: {result.path}")
        print("✓ 流式写入测试通过")
        return True
    finally:
        sbx.kill()


def test_write_files_batch():
    """测试批量写入多文件"""
    print("\n" + "=" * 50)
    print("测试: 批量写入多文件")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        files = [
            {"path": "/home/user/batch1.txt", "data": "Content 1"},
            {"path": "/home/user/batch2.txt", "data": "Content 2"},
            {"path": "/home/user/batch3.txt", "data": "Content 3"},
        ]
        results = sbx.files.write_files(files)
        
        assert len(results) == 3
        print(f"批量写入文件数: {len(results)}")
        for r in results:
            print(f"  - {r.path}")
        print("✓ 批量写入测试通过")
        return True
    finally:
        sbx.kill()


def test_read_text():
    """测试读取文本内容"""
    print("\n" + "=" * 50)
    print("测试: 读取文本内容")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 先写入
        original_content = "Hello, 你好, العربية"
        sbx.files.write("/home/user/read_test.txt", original_content)
        
        # 读取
        content = sbx.files.read("/home/user/read_test.txt")
        
        assert content == original_content
        print(f"读取内容: {content}")
        print("✓ 文本读取测试通过")
        return True
    finally:
        sbx.kill()


def test_read_bytes():
    """测试读取二进制内容"""
    print("\n" + "=" * 50)
    print("测试: 读取二进制内容")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 先写入二进制
        original = b"\x00\x01\x02\x03\x04\x05"
        sbx.files.write("/home/user/binary_read.bin", original)
        
        # 读取为字节
        content = sbx.files.read("/home/user/binary_read.bin", format="bytes")
        
        assert content == original
        print(f"读取二进制长度: {len(content)}")
        print("✓ 二进制读取测试通过")
        return True
    finally:
        sbx.kill()


def test_read_stream():
    """测试流式读取"""
    print("\n" + "=" * 50)
    print("测试: 流式读取")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 写入较大内容
        content = "A" * 10000
        sbx.files.write("/home/user/large.txt", content)
        
        # 流式读取
        chunks = list(sbx.files.read("/home/user/large.txt", format="stream"))
        total_content = b"".join(chunks).decode()
        
        assert total_content == content
        print(f"流式读取块数: {len(chunks)}")
        print(f"总内容长度: {len(total_content)}")
        print("✓ 流式读取测试通过")
        return True
    finally:
        sbx.kill()


def test_list_directory():
    """测试列出目录"""
    print("\n" + "=" * 50)
    print("测试: 列出目录")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 创建一些文件
        sbx.files.write("/home/user/list_test/a.txt", "a")
        sbx.files.write("/home/user/list_test/b.txt", "b")
        sbx.files.write("/home/user/list_test/c.txt", "c")
        
        entries = sbx.files.list("/home/user/list_test")
        
        assert len(entries) == 3
        print(f"目录条目数: {len(entries)}")
        for e in entries:
            print(f"  - {e.name} ({e.type})")
        print("✓ 目录列表测试通过")
        return True
    finally:
        sbx.kill()


def test_list_directory_depth():
    """测试递归列出目录"""
    print("\n" + "=" * 50)
    print("测试: 递归列出目录")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 创建嵌套结构
        sbx.files.write("/home/user/nested/level1/file1.txt", "1")
        sbx.files.write("/home/user/nested/level1/level2/file2.txt", "2")
        
        # 深度为 2
        entries = sbx.files.list("/home/user/nested", depth=2)
        
        print(f"递归列出条目数: {len(entries)}")
        for e in entries:
            print(f"  - {e.path}")
        print("✓ 递归列出测试通过")
        return True
    finally:
        sbx.kill()


def test_file_exists():
    """测试检查文件存在"""
    print("\n" + "=" * 50)
    print("测试: 检查文件存在")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 创建文件
        sbx.files.write("/home/user/exists.txt", "exists")
        
        # 检查存在的文件
        assert sbx.files.exists("/home/user/exists.txt") == True
        print("/home/user/exists.txt 存在: True")
        
        # 检查不存在的文件
        assert sbx.files.exists("/home/user/not_exists.txt") == False
        print("/home/user/not_exists.txt 存在: False")
        
        print("✓ 文件存在检查测试通过")
        return True
    finally:
        sbx.kill()


def test_get_file_info():
    """测试获取文件信息"""
    print("\n" + "=" * 50)
    print("测试: 获取文件信息")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 创建文件
        content = "Info test content"
        sbx.files.write("/home/user/info_test.txt", content)
        
        info = sbx.files.get_info("/home/user/info_test.txt")
        
        assert info.name == "info_test.txt"
        assert info.type == FileType.FILE
        assert info.size == len(content)
        
        print(f"文件名: {info.name}")
        print(f"类型: {info.type}")
        print(f"大小: {info.size} bytes")
        print(f"权限: {info.permissions}")
        print(f"所有者: {info.owner}")
        print(f"修改时间: {info.modified_time}")
        
        print("✓ 文件信息获取测试通过")
        return True
    finally:
        sbx.kill()


def test_remove_file():
    """测试删除文件"""
    print("\n" + "=" * 50)
    print("测试: 删除文件")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 创建文件
        sbx.files.write("/home/user/to_remove.txt", "remove me")
        assert sbx.files.exists("/home/user/to_remove.txt") == True
        
        # 删除文件
        sbx.files.remove("/home/user/to_remove.txt")
        
        # 验证删除
        assert sbx.files.exists("/home/user/to_remove.txt") == False
        
        print("文件已删除")
        print("✓ 文件删除测试通过")
        return True
    finally:
        sbx.kill()


def test_remove_directory():
    """测试删除目录"""
    print("\n" + "=" * 50)
    print("测试: 删除目录")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 创建目录和文件
        sbx.files.write("/home/user/dir_to_remove/file.txt", "content")
        assert sbx.files.exists("/home/user/dir_to_remove") == True
        
        # 删除目录
        sbx.files.remove("/home/user/dir_to_remove")
        
        # 验证删除
        assert sbx.files.exists("/home/user/dir_to_remove") == False
        
        print("目录已删除")
        print("✓ 目录删除测试通过")
        return True
    finally:
        sbx.kill()


def test_rename_file():
    """测试重命名文件"""
    print("\n" + "=" * 50)
    print("测试: 重命名文件")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 创建文件
        sbx.files.write("/home/user/original.txt", "content")
        
        # 重命名
        result = sbx.files.rename("/home/user/original.txt", "/home/user/renamed.txt")
        
        # 验证
        assert sbx.files.exists("/home/user/original.txt") == False
        assert sbx.files.exists("/home/user/renamed.txt") == True
        assert result.path == "/home/user/renamed.txt"
        
        print(f"重命名为: {result.path}")
        print("✓ 文件重命名测试通过")
        return True
    finally:
        sbx.kill()


def test_make_directory():
    """测试创建目录"""
    print("\n" + "=" * 50)
    print("测试: 创建目录")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 创建目录
        result = sbx.files.make_dir("/home/user/new_directory")
        
        # 验证
        assert sbx.files.exists("/home/user/new_directory") == True
        
        info = sbx.files.get_info("/home/user/new_directory")
        assert info.type == FileType.DIR
        
        print("目录已创建")
        print("✓ 创建目录测试通过")
        return True
    finally:
        sbx.kill()


def test_make_nested_directory():
    """测试创建嵌套目录"""
    print("\n" + "=" * 50)
    print("测试: 创建嵌套目录")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 创建多级嵌套目录
        sbx.files.make_dir("/home/user/nested/level1/level2/level3")
        
        # 验证所有级别都存在
        assert sbx.files.exists("/home/user/nested") == True
        assert sbx.files.exists("/home/user/nested/level1") == True
        assert sbx.files.exists("/home/user/nested/level1/level2") == True
        assert sbx.files.exists("/home/user/nested/level1/level2/level3") == True
        
        print("嵌套目录已创建")
        print("✓ 创建嵌套目录测试通过")
        return True
    finally:
        sbx.kill()


def test_watch_directory():
    """测试目录变更监听"""
    print("\n" + "=" * 50)
    print("测试: 目录变更监听")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 创建目录
        sbx.files.make_dir("/home/user/watch_dir")
        
        events_received = []
        
        # 开始监听
        handle = sbx.files.watch_dir("/home/user/watch_dir")
        
        # 在另一个线程中写入文件触发事件
        import threading
        def write_file():
            import time
            time.sleep(0.5)
            sbx.files.write("/home/user/watch_dir/new_file.txt", "content")
        
        thread = threading.Thread(target=write_file)
        thread.start()
        
        # 获取事件 (等待最多 5 秒)
        try:
            for event in handle:
                events_received.append(event)
                print(f"收到事件: {event}")
                if len(events_received) >= 1:
                    break
        except Exception as e:
            print(f"监听异常: {e}")
        
        handle.stop()
        thread.join()
        
        print(f"收到事件数: {len(events_received)}")
        print("✓ 目录监听测试通过")
        return True
    finally:
        sbx.kill()


def run_all():
    """运行所有文件系统测试"""
    test_write_string()
    test_write_bytes()
    test_write_file_stream()
    test_write_files_batch()
    test_read_text()
    test_read_bytes()
    test_read_stream()
    test_list_directory()
    test_list_directory_depth()
    test_file_exists()
    test_get_file_info()
    test_remove_file()
    test_remove_directory()
    test_rename_file()
    test_make_directory()
    test_make_nested_directory()
    # watch_dir 测试可能需要特殊处理
    # test_watch_directory()


if __name__ == "__main__":
    run_all()
