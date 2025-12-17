"""
模板构建脚本 - 构建自定义 E2B 模板
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)
from e2b import Template, CopyItem, default_build_logger, wait_for_timeout


def build_base_template():
    """构建基础模板"""
    print("=" * 50)
    print("构建: 基础模板")
    print("=" * 50)
    
    template = Template().from_base_image()
    
    Template.build(
        template,
        alias="base",
        cpu_count=2,
        memory_mb=512,
        on_build_logs=default_build_logger(),
    )
    
    print("✓ 基础模板构建完成")


def build_code_interpreter_template():
    """构建代码解释器模板"""
    print("=" * 50)
    print("构建: 代码解释器模板")
    print("=" * 50)
    
    template = (
        Template()
        .from_image("uhub.service.ucloud.cn/agentbox/code-interpreter:v1")
        .set_start_cmd(
            "'/bin/sh' '-c' 'sudo /root/.jupyter/start-up.sh'",
            wait_for_timeout(25000)
        )
    )
    
    Template.build(
        template,
        alias="code-interpreter-v1",
        cpu_count=2,
        memory_mb=2048,
        on_build_logs=default_build_logger(),
    )
    
    print("✓ 代码解释器模板构建完成")


def build_desktop_template():
    """构建桌面模板"""
    print("=" * 50)
    print("构建: 桌面模板")
    print("=" * 50)
    
    template = (
        Template(file_context_path="files")
        .from_image("uhub.service.ucloud.cn/clientfzzf/e2b-desktop:v2")
        .set_user("user")
        .set_workdir("/home/user")
    )
    
    Template.build(
        template,
        alias="desktop",
        cpu_count=8,
        memory_mb=8192,
        on_build_logs=default_build_logger(),
    )
    
    print("✓ 桌面模板构建完成")


def get_dockerfile(template_type="base"):
    """获取 Dockerfile 内容"""
    if template_type == "base":
        template = Template().from_base_image()
    elif template_type == "desktop":
        template = (
            Template(file_context_path="files")
            .from_image("uhub.service.ucloud.cn/clientfzzf/e2b-desktop:v2")
        )
    else:
        template = Template().from_base_image()
    
    return Template.to_dockerfile(template)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python build_template.py <template_type>")
        print("  template_type: base | code-interpreter | desktop | dockerfile")
        sys.exit(1)
    
    template_type = sys.argv[1]
    
    if template_type == "base":
        build_base_template()
    elif template_type == "code-interpreter":
        build_code_interpreter_template()
    elif template_type == "desktop":
        build_desktop_template()
    elif template_type == "dockerfile":
        print(get_dockerfile())
    else:
        print(f"未知模板类型: {template_type}")
        sys.exit(1)
