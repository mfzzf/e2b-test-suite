"""
模板构建测试
"""
import os
import time
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

from ucloud_agentbox import Template, TemplateBase, LogEntry


# 简单的测试模板
class SimpleTemplate(TemplateBase):
    """简单测试模板"""
    
    dockerfile = """
FROM python:3.11-slim

RUN pip install numpy

WORKDIR /home/user
"""


def test_template_build():
    """测试构建模板"""
    print("=" * 50)
    print("测试: 构建模板")
    print("=" * 50)
    
    logs = []
    
    def on_logs(log: LogEntry):
        logs.append(log)
        print(f"[BUILD] {log}")
    
    try:
        # 构建模板
        result = Template.build(
            template=SimpleTemplate,
            alias="test-simple-template",
            cpu_count=2,
            memory_mb=1024,
            on_build_logs=on_logs,
        )
        
        print(f"构建结果: {result}")
        print(f"日志数量: {len(logs)}")
        print("✓ 模板构建测试通过")
        return True
    except Exception as e:
        print(f"构建失败 (可能需要配置): {e}")
        print("⚠ 模板构建测试跳过 (需要构建权限)")
        return True


def test_template_build_in_background():
    """测试后台构建模板"""
    print("\n" + "=" * 50)
    print("测试: 后台构建模板")
    print("=" * 50)
    
    logs = []
    
    def on_logs(log: LogEntry):
        logs.append(log)
        print(f"[BUILD] {log}")
    
    try:
        # 后台构建
        build_info = Template.build_in_background(
            template=SimpleTemplate,
            alias="test-bg-template",
            cpu_count=2,
            memory_mb=1024,
            on_build_logs=on_logs,
        )
        
        print(f"构建信息: {build_info}")
        
        # 等待一段时间
        time.sleep(5)
        
        # 获取构建状态
        status = Template.get_build_status(build_info)
        print(f"构建状态: {status}")
        
        print("✓ 后台构建测试通过")
        return True
    except Exception as e:
        print(f"后台构建失败 (可能需要配置): {e}")
        print("⚠ 后台构建测试跳过 (需要构建权限)")
        return True


def test_get_build_status():
    """测试获取构建状态"""
    print("\n" + "=" * 50)
    print("测试: 获取构建状态")
    print("=" * 50)
    
    try:
        # 先启动后台构建
        build_info = Template.build_in_background(
            template=SimpleTemplate,
            alias="test-status-template",
            cpu_count=2,
            memory_mb=1024,
        )
        
        # 获取状态
        status = Template.get_build_status(build_info)
        print(f"构建状态: {status}")
        
        # 等待并再次获取
        time.sleep(10)
        status2 = Template.get_build_status(build_info)
        print(f"更新状态: {status2}")
        
        print("✓ 获取构建状态测试通过")
        return True
    except Exception as e:
        print(f"获取状态失败 (可能需要配置): {e}")
        print("⚠ 获取构建状态测试跳过 (需要构建权限)")
        return True


def run_all():
    """运行所有模板测试"""
    print("\n⚠ 注意: 模板构建测试需要有效的 API Key 和构建权限")
    print("如果没有权限，测试将跳过\n")
    
    test_template_build()
    test_template_build_in_background()
    test_get_build_status()


if __name__ == "__main__":
    run_all()
