"""
沙箱信息与监控测试 - 获取信息、指标监控
"""
import os
import time
import datetime
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

from ucloud_agentbox import Sandbox, SandboxInfo, SandboxMetrics


def test_get_info():
    """测试获取沙箱基本信息"""
    print("=" * 50)
    print("测试: 获取沙箱信息")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        info = sbx.get_info()
        
        assert info.sandbox_id == sbx.sandbox_id
        print(f"沙箱 ID: {info.sandbox_id}")
        print(f"模板 ID: {info.template_id}")
        print(f"创建时间: {info.started_at}")
        print(f"结束时间: {info.end_at}")
        
        print("✓ 获取沙箱信息测试通过")
        return True
    finally:
        sbx.kill()


def test_get_info_fields():
    """测试验证信息字段完整性"""
    print("\n" + "=" * 50)
    print("测试: 验证信息字段")
    print("=" * 50)
    
    metadata = {"test_key": "test_value"}
    sbx = Sandbox.create(metadata=metadata, timeout=300)
    try:
        info = sbx.get_info()
        
        # 验证必要字段存在
        assert hasattr(info, 'sandbox_id')
        assert hasattr(info, 'template_id')
        assert hasattr(info, 'started_at')
        assert hasattr(info, 'end_at')
        assert hasattr(info, 'metadata')
        
        # 验证元数据
        assert info.metadata.get("test_key") == "test_value"
        
        print("字段检查:")
        print(f"  - sandbox_id: {info.sandbox_id}")
        print(f"  - template_id: {info.template_id}")
        print(f"  - started_at: {info.started_at}")
        print(f"  - end_at: {info.end_at}")
        print(f"  - metadata: {info.metadata}")
        
        print("✓ 信息字段验证测试通过")
        return True
    finally:
        sbx.kill()


def test_get_info_by_id():
    """测试通过 ID 获取沙箱信息"""
    print("\n" + "=" * 50)
    print("测试: 通过 ID 获取信息")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    sandbox_id = sbx.sandbox_id
    
    try:
        # 使用类方法通过 ID 获取信息
        info = Sandbox.get_info(sandbox_id)
        
        assert info.sandbox_id == sandbox_id
        print(f"通过 ID 获取沙箱信息成功: {info.sandbox_id}")
        print("✓ 通过 ID 获取信息测试通过")
        return True
    finally:
        sbx.kill()


def test_get_metrics():
    """测试获取资源指标"""
    print("\n" + "=" * 50)
    print("测试: 获取资源指标")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 执行一些操作产生资源使用
        sbx.commands.run("echo 'Hello World'")
        sbx.files.write("/home/user/test.txt", "Test content")
        
        # 等待一点时间让指标收集
        time.sleep(2)
        
        metrics = sbx.get_metrics()
        
        print(f"指标数量: {len(metrics)}")
        
        if len(metrics) > 0:
            m = metrics[0]
            print(f"CPU 使用: {m.cpu_pct if hasattr(m, 'cpu_pct') else 'N/A'}%")
            print(f"内存使用: {m.mem_mb if hasattr(m, 'mem_mb') else 'N/A'} MB")
        
        print("✓ 获取资源指标测试通过")
        return True
    finally:
        sbx.kill()


def test_get_metrics_with_time_range():
    """测试指定时间范围的指标"""
    print("\n" + "=" * 50)
    print("测试: 时间范围指标")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    try:
        # 记录开始时间
        start_time = datetime.datetime.now(datetime.timezone.utc)
        
        # 执行操作
        sbx.commands.run("sleep 1")
        sbx.commands.run("echo 'test'")
        
        # 记录结束时间
        end_time = datetime.datetime.now(datetime.timezone.utc)
        
        # 获取指定时间范围的指标
        metrics = sbx.get_metrics(start=start_time, end=end_time)
        
        print(f"时间范围: {start_time} - {end_time}")
        print(f"指标数量: {len(metrics)}")
        
        print("✓ 时间范围指标测试通过")
        return True
    finally:
        sbx.kill()


def test_get_metrics_by_id():
    """测试通过 ID 获取指标"""
    print("\n" + "=" * 50)
    print("测试: 通过 ID 获取指标")
    print("=" * 50)
    
    sbx = Sandbox.create(timeout=300)
    sandbox_id = sbx.sandbox_id
    
    try:
        # 执行操作
        sbx.commands.run("echo 'Hello'")
        time.sleep(1)
        
        # 使用类方法通过 ID 获取指标
        metrics = Sandbox.get_metrics(sandbox_id)
        
        print(f"通过 ID 获取指标数量: {len(metrics)}")
        print("✓ 通过 ID 获取指标测试通过")
        return True
    finally:
        sbx.kill()


def run_all():
    """运行所有信息监控测试"""
    test_get_info()
    test_get_info_fields()
    test_get_info_by_id()
    test_get_metrics()
    test_get_metrics_with_time_range()
    test_get_metrics_by_id()


if __name__ == "__main__":
    run_all()
