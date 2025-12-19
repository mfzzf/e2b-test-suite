"""
UHub 私有仓库测试
测试使用 UCloud UHub 私有仓库作为基础镜像
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

from ucloud_sandbox import Template, TemplateBase, LogEntry


class UHubTemplate(TemplateBase):
    """使用 UHub 私有镜像的模板"""
    
    def template(self):
        return (
            Template()
            .from_uhub_registry(
                image=os.environ.get("UHUB_IMAGE", "uhub.service.ucloud.cn/agentbox/code-interpreter:v1"),
                username=os.environ.get("UHUB_USERNAME", ""),
                password=os.environ.get("UHUB_PASSWORD", ""),
            )
            .run_cmd("echo 'UHub registry test'")
        )


def test_uhub_registry_template_creation():
    """测试 UHub 私有仓库模板创建"""
    print("=" * 50)
    print("测试: UHub 私有仓库模板创建")
    print("=" * 50)
    
    try:
        # 创建模板
        template = (
            Template()
            .from_uhub_registry(
                image="uhub.service.ucloud.cn/agentbox/code-interpreter:v1",
                username="test@ucloud.cn",
                password="test-password",
            )
            .run_cmd("pip install numpy")
        )
        
        # 验证模板已创建
        assert template is not None
        assert template._template._base_image == "uhub.service.ucloud.cn/agentbox/code-interpreter:v1"
        assert template._template._registry_config is not None
        assert template._template._registry_config["type"] == "uhub"
        assert template._template._registry_config["username"] == "test@ucloud.cn"
        assert template._template._registry_config["password"] == "test-password"
        
        print("✓ UHub 模板创建验证通过")
        print(f"  - 基础镜像: {template._template._base_image}")
        print(f"  - 仓库类型: {template._template._registry_config['type']}")
        print(f"  - 用户名: {template._template._registry_config['username']}")
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False


def test_uhub_registry_to_json():
    """测试 UHub 模板转换为 JSON"""
    print("\n" + "=" * 50)
    print("测试: UHub 模板转换为 JSON")
    print("=" * 50)
    
    try:
        template = (
            Template()
            .from_uhub_registry(
                image="uhub.service.ucloud.cn/agentbox/code-interpreter:v1",
                username="test@ucloud.cn",
                password="test-password",
            )
            .run_cmd("apt-get update")
        )
        
        # 转换为 JSON
        json_str = TemplateBase.to_json(template)
        
        assert "uhub.service.ucloud.cn/agentbox/code-interpreter:v1" in json_str
        assert "uhub" in json_str
        
        print(f"✓ JSON 转换成功")
        print(f"  JSON 内容: {json_str[:200]}...")
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False


def test_uhub_registry_build():
    """测试使用 UHub 私有仓库构建模板（需要有效凭据）"""
    print("\n" + "=" * 50)
    print("测试: UHub 私有仓库构建模板")
    print("=" * 50)
    
    # 检查环境变量
    uhub_image = os.environ.get("UHUB_IMAGE")
    uhub_username = os.environ.get("UHUB_USERNAME")
    uhub_password = os.environ.get("UHUB_PASSWORD")
    
    if not all([uhub_image, uhub_username, uhub_password]):
        print("⚠ 跳过: 缺少 UHUB_IMAGE, UHUB_USERNAME 或 UHUB_PASSWORD 环境变量")
        print("  请设置以下环境变量后重试:")
        print("    export UHUB_IMAGE=uhub.service.ucloud.cn/your-org/your-image:tag")
        print("    export UHUB_USERNAME=your-username")
        print("    export UHUB_PASSWORD=your-password")
        return True
    
    logs = []
    
    def on_logs(log: LogEntry):
        logs.append(log)
        print(f"[BUILD] {log}")
    
    try:
        result = Template.build(
            template=UHubTemplate,
            alias="test-uhub-template",
            cpu_count=2,
            memory_mb=1024,
            on_build_logs=on_logs,
        )
        
        print(f"✓ UHub 模板构建成功")
        print(f"  构建结果: {result}")
        print(f"  日志数量: {len(logs)}")
        return True
    except Exception as e:
        print(f"✗ 构建失败: {e}")
        return False


def run_all():
    """运行所有 UHub 仓库测试"""
    from tests.conftest import run_tests_safely
    
    print("\n" + "=" * 60)
    print("UHub 私有仓库测试套件")
    print("=" * 60)
    
    tests = [
        test_uhub_registry_template_creation,
        test_uhub_registry_to_json,
        test_uhub_registry_build,
    ]
    run_tests_safely(tests, "uhub_registry")


if __name__ == "__main__":
    run_all()
