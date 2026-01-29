# Contributing to Investment Research Orchestrator

Thank you for your interest in contributing to the Investment Research Orchestrator! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Maintain a professional and friendly environment

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)
- Error messages and stack traces

### Suggesting Features

Feature suggestions are welcome! Please include:
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach
- Any relevant examples or mockups

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Write/update tests**
5. **Update documentation**
6. **Commit with clear messages**: Use conventional commit format
7. **Push to your fork**
8. **Create a Pull Request**

## Development Setup

### Prerequisites
- Python 3.11 or higher
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Learn.git
cd Learn/investment_orchestrator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio pytest-cov black flake8 mypy

# Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Use meaningful variable names

**Formatting with Black:**
```bash
black src/ tests/
```

**Linting with flake8:**
```bash
flake8 src/ tests/ --max-line-length=100
```

**Type checking with mypy:**
```bash
mypy src/
```

### Documentation

- Update README.md for new features
- Add docstrings to all public APIs
- Update example_queries.md for new capabilities
- Include inline comments for complex logic
- Update CHANGELOG.md

### Testing

- Write tests for all new features
- Maintain or improve test coverage
- Use mocking for external dependencies
- Test both success and error cases

**Running tests:**
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_orchestrator.py::test_function_name -v
```

### Commit Messages

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Build/tooling changes

Examples:
```
feat(tools): add new risk assessment tool

fix(api_client): handle timeout errors properly

docs(readme): update installation instructions
```

## Pull Request Process

1. **Ensure tests pass**: All tests must pass before merging
2. **Update documentation**: Keep docs in sync with code changes
3. **Add changelog entry**: Document your changes in CHANGELOG.md
4. **Request review**: Tag maintainers for review
5. **Address feedback**: Respond to review comments promptly
6. **Squash commits**: Clean up commit history if needed

### PR Checklist

- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Code follows style guidelines
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or clearly documented)
- [ ] PR description explains the change

## Project Structure

```
investment_orchestrator/
├── src/                    # Source code
│   ├── orchestrator.py    # Main FastAPI app
│   ├── api_client.py      # HTTP client
│   ├── config.py          # Configuration
│   └── tools/             # LangChain tools
├── tests/                 # Test suite
├── examples/              # Example queries
├── java_backend_reference/# Java backend reference
├── docs/                  # Additional documentation
└── requirements.txt       # Python dependencies
```

## Adding New Tools

To add a new LangChain tool:

1. Create `src/tools/your_tool.py`:
```python
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from ..api_client import api_client

class YourToolInput(BaseModel):
    param: str = Field(description="Parameter description")

async def your_tool_impl(param: str) -> str:
    # Implementation
    result = await api_client.your_method(param)
    return f"Result: {result}"

your_tool = StructuredTool.from_function(
    coroutine=your_tool_impl,
    name="YourTool",
    description="Tool description for LLM",
    args_schema=YourToolInput,
)
```

2. Update `src/tools/__init__.py`:
```python
from .your_tool import your_tool
__all__ = [..., "your_tool"]
```

3. Register in `src/orchestrator.py`:
```python
tools = [
    ...,
    your_tool,
]
```

4. Add tests in `tests/test_orchestrator.py`

5. Update documentation

## Getting Help

- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the [README](README.md) and [examples](examples/)

## Recognition

Contributors will be:
- Listed in the project contributors
- Credited in release notes
- Mentioned in documentation

Thank you for contributing to the Investment Research Orchestrator! 🚀
