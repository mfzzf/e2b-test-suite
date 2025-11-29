#!/usr/bin/env python3
"""
E2B 测试套件运行入口
"""
import sys
import argparse
import traceback
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 测试模块映射
TEST_MODULES = {
    "sandbox_basic": "tests.test_sandbox_basic",
    "file_operations": "tests.test_file_operations",
    "code_execution": "tests.test_code_execution",
    "streaming": "tests.test_streaming",
    "charts": "tests.test_charts",
    "desktop": "tests.test_desktop",
    "openai": "tests.test_openai_integration",
}


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
    parser = argparse.ArgumentParser(description="E2B 测试套件")
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
    
    args = parser.parse_args()
    
    if args.list:
        print("可用测试:")
        for name in TEST_MODULES:
            print(f"  - {name}")
        return
    
    if args.test:
        success = run_test(args.test)
        sys.exit(0 if success else 1)
    else:
        results = run_all_tests()
        print_summary(results)
        
        failed = sum(1 for v in results.values() if not v)
        sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
