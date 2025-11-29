"""
OpenAI 集成测试 - 函数调用与代码执行
"""
import os
import json
from dotenv import load_dotenv
load_dotenv(override=True)

# 确保环境变量已加载后再导入 e2b
from openai import OpenAI
from e2b_code_interpreter import Sandbox


# 工具定义
TOOLS = [{
    "type": "function",
    "function": {
        "name": "execute_python",
        "description": "Execute python code in a Jupyter notebook cell and return result",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The python code to execute in a single cell"
                }
            },
            "required": ["code"]
        }
    }
}]


def test_openai_code_execution():
    """测试 OpenAI 函数调用执行代码"""
    print("=" * 50)
    print("测试: OpenAI 函数调用")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    if not api_key:
        print("⚠ 未配置 OPENAI_API_KEY，跳过测试")
        return True
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    messages = [
        {"role": "user", "content": "Calculate how many r's are in the word 'strawberry'"}
    ]
    
    # 第一次调用
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS,
    )
    
    response_message = response.choices[0].message
    messages.append(response_message)
    
    # 执行工具调用
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "execute_python":
                print("创建沙箱执行代码...")
                
                with Sandbox.create() as sandbox:
                    code = json.loads(tool_call.function.arguments)['code']
                    print(f"执行代码: {code[:100]}...")
                    
                    execution = sandbox.run_code(code)
                    result = execution.text
                    print(f"执行结果: {result}")
                
                messages.append({
                    "role": "tool",
                    "name": "execute_python",
                    "content": result,
                    "tool_call_id": tool_call.id,
                })
        
        # 最终响应
        final_response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        print(f"最终回答: {final_response.choices[0].message.content}")
    else:
        print("模型未调用工具")
    
    print("✓ OpenAI 集成测试通过")
    return True


def test_simple_chat():
    """测试简单对话"""
    print("\n" + "=" * 50)
    print("测试: 简单对话")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    if not api_key:
        print("⚠ 未配置 OPENAI_API_KEY，跳过测试")
        return True
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say hello in Chinese"}],
    )
    
    print(f"回答: {response.choices[0].message.content}")
    print("✓ 简单对话测试通过")
    return True


def run_all():
    """运行所有 OpenAI 集成测试"""
    test_simple_chat()
    test_openai_code_execution()


if __name__ == "__main__":
    run_all()
