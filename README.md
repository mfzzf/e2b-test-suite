# UCloud AgentBox 后端服务测试套件

UCloud AgentBox (`ucloud-agentbox`) Python SDK 的完整测试脚本集合。

## 项目结构

```
e2b-test-suite/
├── tests/
│   ├── conftest.py               # pytest 配置和共享 fixtures
│   ├── test_sandbox_lifecycle.py # 沙箱生命周期测试 (12 tests)
│   ├── test_sandbox_info.py      # 沙箱信息监控测试 (6 tests)
│   ├── test_filesystem_complete.py # 完整文件系统测试 (17 tests)
│   ├── test_commands_complete.py # 完整命令执行测试 (15 tests)
│   ├── test_pty_complete.py      # PTY 伪终端测试 (7 tests)
│   ├── test_async_sandbox.py     # 异步 API 测试 (10 tests)
│   ├── test_template_build.py    # 模板构建测试 (3 tests)
│   ├── test_exceptions.py        # 异常处理测试 (9 tests)
│   └── (旧版测试文件...)
├── templates/
│   └── build_template.py         # 模板构建脚本
├── requirements.txt
└── run_tests.py                  # 测试运行入口
```

## 安装

```bash
cd e2b-test-suite

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖 (包含本地 SDK)
pip install -r requirements.txt
```

## 配置

1. 复制环境变量配置文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的 API Key：
```
AGENTBOX_API_KEY=your_api_key
E2B_API_KEY=your_api_key
```

## 运行测试

```bash
# 运行核心测试 (默认)
python run_tests.py

# 运行所有测试
python run_tests.py --all

# 运行单个测试模块
python run_tests.py --test sandbox_lifecycle
python run_tests.py --test filesystem_complete
python run_tests.py --test commands_complete
python run_tests.py --test async_sandbox

# 列出所有可用测试
python run_tests.py --list

# 使用 pytest 运行
pytest tests/ -v
```

## 测试模块说明

| 测试模块 | 说明 | 测试数 |
|---------|------|-------|
| sandbox_lifecycle | 沙箱创建、连接、暂停、恢复、销毁 | 12 |
| sandbox_info | 沙箱信息获取、资源指标监控 | 6 |
| filesystem_complete | 文件读写、列表、删除、重命名、目录操作 | 17 |
| commands_complete | 命令执行、进程管理、输入输出回调 | 15 |
| pty_complete | PTY 创建、输入、调整大小、终止 | 7 |
| async_sandbox | AsyncSandbox 异步 API 完整测试 | 10 |
| template_build | 模板构建与状态查询 (需特殊权限) | 3 |
| exceptions | 异常处理和边界情况测试 | 9 |

## 旧版兼容测试

旧版 E2B 测试仍然保留，可单独运行：

| 测试模块 | 说明 |
|---------|------|
| sandbox_basic | 基础沙箱测试 |
| file_operations | 文件上传下载测试 |
| code_execution | Python 代码执行测试 |
| streaming | 流式输出 (stdout/stderr) |
| charts | Matplotlib 图表生成与解析 |
| desktop | 桌面沙箱、VNC 流、应用启动 |
| openai | OpenAI 函数调用集成 |
