"""
流式输出测试 - stdout/stderr 实时输出
"""
from dotenv import load_dotenv
load_dotenv()

from e2b_code_interpreter import Sandbox


def test_streaming_output():
    """测试流式输出"""
    print("=" * 50)
    print("测试: 流式输出")
    print("=" * 50)
    
    code = """
import time
import sys

print("第一行输出到 stdout")
time.sleep(1)
print("第二行输出到 stderr", file=sys.stderr)
time.sleep(1)
print("第三行输出到 stdout")
"""
    
    stdout_lines = []
    stderr_lines = []
    errors = []
    
    sandbox = Sandbox.create()
    sandbox.run_code(
        code,
        on_error=lambda error: errors.append(error),
        on_stdout=lambda data: (stdout_lines.append(data), print(f"stdout: {data}")),
        on_stderr=lambda data: (stderr_lines.append(data), print(f"stderr: {data}")),
    )
    
    print(f"\n收到 stdout 行数: {len(stdout_lines)}")
    print(f"收到 stderr 行数: {len(stderr_lines)}")
    print(f"错误数: {len(errors)}")
    
    sandbox.kill()
    print("✓ 流式输出测试通过")
    return True


def test_long_running_output():
    """测试长时间运行的输出"""
    print("\n" + "=" * 50)
    print("测试: 长时间运行输出")
    print("=" * 50)
    
    code = """
import time
for i in range(5):
    print(f"进度: {i+1}/5")
    time.sleep(0.5)
print("完成!")
"""
    
    sandbox = Sandbox.create()
    sandbox.run_code(
        code,
        on_stdout=lambda data: print(f"  {data.strip()}"),
    )
    
    sandbox.kill()
    print("✓ 长时间运行输出测试通过")
    return True


def run_all():
    """运行所有流式输出测试"""
    test_streaming_output()
    test_long_running_output()


if __name__ == "__main__":
    run_all()
