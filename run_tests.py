#!/usr/bin/env python3
"""
UCloud AgentBox SDK 测试套件运行入口
"""
import os
import sys
from pathlib import Path

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent / ".env"
from dotenv import load_dotenv
load_dotenv(env_path, override=True)

# 设置环境变量供子模块使用
os.environ["E2B_ENV_PATH"] = str(env_path)

import argparse
import traceback

# 测试模块映射
TEST_MODULES = {
    "sandbox_lifecycle": "tests.test_sandbox_lifecycle",
    "sandbox_info": "tests.test_sandbox_info",
    "filesystem_complete": "tests.test_filesystem_complete",
    "commands_complete": "tests.test_commands_complete",
    "pty_complete": "tests.test_pty_complete",
    "async_sandbox": "tests.test_async_sandbox",
    "template_build": "tests.test_template_build",
    "exceptions": "tests.test_exceptions",
}

# 新 SDK 核心测试组
CORE_TESTS = [
    "sandbox_lifecycle",
    "sandbox_info",
    "filesystem_complete",
    "commands_complete",
    "pty_complete",
    "async_sandbox",
    "exceptions",
]


def run_test(test_name: str) -> bool:
    """运行单个测试模块"""
    if test_name not in TEST_MODULES:
        print(f"❌ 未知测试: {test_name}")
        print(f"可用测试: {', '.join(TEST_MODULES.keys())}")
        return False
    
    module_name = TEST_MODULES[test_name]
    
    try:
        print(f"\n{'#' * 60}")
        print(f"# 运行测试: {test_name}")
        print(f"{'#' * 60}\n")
        
        module = __import__(module_name, fromlist=["run_all"])
        module.run_all()
        
        print(f"\n✅ 测试 {test_name} 完成")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试 {test_name} 失败: {e}")
        traceback.print_exc()
        return False


def run_all_tests() -> dict:
    """运行所有测试"""
    results = {}
    
    for test_name in TEST_MODULES:
        results[test_name] = run_test(test_name)
    
    return results


def run_core_tests() -> dict:
    """运行核心测试"""
    results = {}
    
    for test_name in CORE_TESTS:
        results[test_name] = run_test(test_name)
    
    return results


def print_summary(results: dict):
    """打印测试摘要"""
    print("\n" + "=" * 60)
    print("测试摘要")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    failed = sum(1 for v in results.values() if not v)
    
    for name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    print("-" * 60)
    print(f"总计: {passed} 通过, {failed} 失败")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="UCloud AgentBox SDK 测试套件")
    parser.add_argument(
        "--test", "-t",
        type=str,
        help=f"运行指定测试 ({', '.join(TEST_MODULES.keys())})"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="列出所有可用测试"
    )
    parser.add_argument(
        "--core", "-c",
        action="store_true",
        help="只运行核心测试"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="运行所有测试"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("可用测试:")
        print("\n核心测试 (ucloud-agentbox SDK):")
        for name in CORE_TESTS:
            print(f"  - {name}")
        print("\n模板测试 (需要特殊权限):")
        print("  - template_build")
        return
    
    if args.test:
        success = run_test(args.test)
        sys.exit(0 if success else 1)
    elif args.core:
        results = run_core_tests()
        print_summary(results)
        failed = sum(1 for v in results.values() if not v)
        sys.exit(0 if failed == 0 else 1)
    elif args.all:
        results = run_all_tests()
        print_summary(results)
        failed = sum(1 for v in results.values() if not v)
        sys.exit(0 if failed == 0 else 1)
    else:
        # 默认运行核心测试
        print("运行核心测试 (使用 --all 运行所有测试)")
        results = run_core_tests()
        print_summary(results)
        failed = sum(1 for v in results.values() if not v)
        sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
