# E2B 后端服务测试套件

E2B (Code Interpreter) 后端服务的测试脚本集合。

## 项目结构

```
e2b-test-suite/
├── config/
│   └── .env.example          # 环境变量配置示例
├── tests/
│   ├── test_sandbox_basic.py      # 基础沙箱测试
│   ├── test_file_operations.py    # 文件上传下载测试
│   ├── test_code_execution.py     # 代码执行测试
│   ├── test_streaming.py          # 流式输出测试
│   ├── test_charts.py             # 图表生成测试
│   ├── test_desktop.py            # 桌面沙箱测试
│   └── test_openai_integration.py # OpenAI 集成测试
├── templates/
│   └── build_template.py     # 模板构建脚本
├── requirements.txt
└── run_tests.py              # 测试运行入口
```

## 安装

```bash
cd e2b-test-suite
pip install -r requirements.txt
```

## 配置

1. 复制环境变量配置文件：
```bash
cp config/.env.example .env
```

2. 编辑 `.env` 文件，填入你的 E2B API Key 和服务地址。

## 运行测试

```bash
# 运行所有测试
python run_tests.py

# 运行单个测试
python run_tests.py --test sandbox_basic
python run_tests.py --test file_operations
python run_tests.py --test code_execution
python run_tests.py --test streaming
python run_tests.py --test charts
python run_tests.py --test desktop
python run_tests.py --test openai
```

## 测试说明

| 测试模块 | 说明 |
|---------|------|
| sandbox_basic | 沙箱创建、连接、信息获取、文件列表 |
| file_operations | 文件上传、下载、读写操作 |
| code_execution | Python 代码执行 |
| streaming | 流式输出 (stdout/stderr) |
| charts | Matplotlib 图表生成与解析 |
| desktop | 桌面沙箱、VNC 流、应用启动 |
| openai | OpenAI 函数调用集成 |
