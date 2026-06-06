# 🧪 Test Generator

AI测试生成器，自动生成单元测试、集成测试、E2E测试。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/OpenAI-API-green?logo=openai" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

## ✨ 特性

- 🧪 单元测试生成
- 🔗 集成测试生成
- 🌐 API测试生成
- 🖥️ E2E测试生成
- 📊 覆盖率分析
- 💡 测试用例建议

## 🚀 快速开始

```bash
pip install openai

python generator.py
```

## 📖 使用

```python
from test_generator import create_generator

generator = create_generator()

# 生成单元测试
tests = generator.generate_unit_tests(code, "Python", "pytest")

# 生成集成测试
tests = generator.generate_integration_tests(code, ["database", "api"])

# 生成API测试
tests = generator.generate_api_tests(api_spec)

# 生成E2E测试
tests = generator.generate_e2e_tests(["用户登录", "添加商品", "下单支付"])

# 分析覆盖率
coverage = generator.analyze_test_coverage(code, tests)

# 建议测试用例
cases = generator.suggest_test_cases("def add(a, b)", "两数相加")
```

## 📁 项目结构

```
test-generator/
├── generator.py   # 测试生成器核心
└── README.md
```

## 📄 许可证

MIT License
