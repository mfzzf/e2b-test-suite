"""
文件操作测试 - 上传、下载、读写
"""
import os
import tempfile
from dotenv import load_dotenv
load_dotenv(override=True)

# 确保环境变量已加载后再导入 e2b
from e2b_code_interpreter import Sandbox


def test_file_upload():
    """测试文件上传"""
    print("=" * 50)
    print("测试: 文件上传")
    print("=" * 50)
    
    sbx = Sandbox.create()
    
    # 创建临时测试文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Hello from test file A")
        temp_file_a = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Hello from test file B")
        temp_file_b = f.name
    
    try:
        # 上传文件
        with open(temp_file_a, "rb") as file:
            sbx.files.write("/home/user/a.txt", file)
            print("✓ 上传文件 a.txt")
        
        with open(temp_file_b, "rb") as file:
            sbx.files.write("/home/user/b.txt", file)
            print("✓ 上传文件 b.txt")
        
        # 验证文件存在
        files = sbx.files.list("/home/user")
        file_names = [f.name for f in files]
        assert "a.txt" in file_names, "a.txt 未找到"
        assert "b.txt" in file_names, "b.txt 未找到"
        print("✓ 文件上传验证通过")
        
    finally:
        os.unlink(temp_file_a)
        os.unlink(temp_file_b)
        sbx.kill()
    
    return True


def test_file_download():
    """测试文件下载"""
    print("\n" + "=" * 50)
    print("测试: 文件下载")
    print("=" * 50)
    
    sbx = Sandbox.create()
    
    # 先写入文件
    test_content = "Test content for download"
    sbx.files.write("/home/user/download_test.txt", test_content)
    
    # 读取文件
    content = sbx.files.read("/home/user/download_test.txt")
    assert content == test_content, f"内容不匹配: {content}"
    print(f"✓ 文件内容: {content}")
    
    sbx.kill()
    print("✓ 文件下载测试通过")
    return True


def test_file_write_string():
    """测试直接写入字符串"""
    print("\n" + "=" * 50)
    print("测试: 字符串写入")
    print("=" * 50)
    
    sbx = Sandbox.create()
    
    # 写入字符串
    sbx.files.write("/home/user/string_test.txt", "直接写入的字符串内容")
    
    # 验证
    content = sbx.files.read("/home/user/string_test.txt")
    print(f"✓ 写入并读取: {content}")
    
    sbx.kill()
    print("✓ 字符串写入测试通过")
    return True


def run_all():
    """运行所有文件操作测试"""
    test_file_upload()
    test_file_download()
    test_file_write_string()


if __name__ == "__main__":
    run_all()
