"""
Test Generator - AI测试生成器
自动生成单元测试、集成测试、E2E测试
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class TestGenerator:
    """
    AI测试生成器
    支持：单元测试、集成测试、E2E测试
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def generate_unit_tests(self, code: str, language: str = "Python", framework: str = "pytest") -> str:
        """生成单元测试"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请为以下{language}代码生成{framework}单元测试：

```{language}
{code}
```

要求：
1. 覆盖所有公共方法
2. 包含正常情况和边界情况
3. 包含错误处理测试
4. 使用{framework}框架
5. 添加清晰的测试说明"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response.choices[0].message.content

    def generate_integration_tests(self, code: str, dependencies: List[str] = None, language: str = "Python") -> str:
        """生成集成测试"""
        if not self.client:
            return "LLM客户端未配置"

        deps = ", ".join(dependencies) if dependencies else "无"

        prompt = f"""请为以下{language}代码生成集成测试：

```{language}
{code}
```

依赖：{deps}

要求：
1. 测试组件间交互
2. Mock外部依赖
3. 测试数据流
4. 包含端到端场景"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response.choices[0].message.content

    def generate_api_tests(self, api_spec: str, framework: str = "pytest") -> str:
        """生成API测试"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请根据以下API规范生成{framework}测试：

{api_spec}

要求：
1. 测试所有端点
2. 包含正常和异常情况
3. 测试认证和授权
4. 测试请求验证
5. 包含性能测试基本用例"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response.choices[0].message.content

    def generate_e2e_tests(self, user_flows: List[str], framework: str = "playwright") -> str:
        """生成E2E测试"""
        if not self.client:
            return "LLM客户端未配置"

        flows = "\n".join(f"- {f}" for f in user_flows)

        prompt = f"""请生成{framework} E2E测试：

用户流程：
{flows}

要求：
1. 覆盖所有用户流程
2. 包含页面交互
3. 包含断言验证
4. 包含等待策略
5. 可读性强"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response.choices[0].message.content

    def analyze_test_coverage(self, code: str, tests: str) -> Dict:
        """分析测试覆盖率"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prompt = f"""请分析以下代码和测试的覆盖率：

代码：
```python
{code}
```

测试：
```python
{tests}
```

请返回JSON格式：
{{
    "coverage_score": 1-100,
    "covered_functions": ["已覆盖的函数"],
    "uncovered_functions": ["未覆盖的函数"],
    "missing_scenarios": ["缺失的测试场景"],
    "recommendations": ["改进建议"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            return {"error": str(e)}

        return {"analysis": content}

    def suggest_test_cases(self, function_signature: str, description: str = "") -> List[Dict]:
        """建议测试用例"""
        if not self.client:
            return [{"error": "LLM客户端未配置"}]

        prompt = f"""请为以下函数建议测试用例：

函数签名：{function_signature}
描述：{description}

请返回JSON格式：
[
    {{"name": "测试名称", "input": "输入", "expected": "预期输出", "type": "normal/boundary/error"}}
]"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            return [{"error": str(e)}]

        return [{"suggestion": content}]

    def save_tests(self, tests: str, file_path: str):
        """保存测试到文件"""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(tests)


def create_generator(**kwargs) -> TestGenerator:
    """创建测试生成器"""
    return TestGenerator(**kwargs)


if __name__ == "__main__":
    generator = create_generator()

    print("Test Generator")
    print()

    # 测试代码
    test_code = """
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class Calculator:
    def __init__(self):
        self.history = []

    def calculate(self, expression):
        result = eval(expression)
        self.history.append((expression, result))
        return result
"""

    print("Generating tests...")
    tests = generator.generate_unit_tests(test_code, "Python", "pytest")
    print(tests[:500] + "...")
