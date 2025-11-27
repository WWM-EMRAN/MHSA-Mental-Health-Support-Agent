# Contributing to MHSA

Thank you for your interest in contributing to the Mental Health Support Agent! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

### Our Pledge

This project is focused on mental health support, and we are committed to:

- **Compassion**: Treating all contributors with kindness and respect
- **Inclusivity**: Welcoming contributors from all backgrounds
- **Safety**: Prioritizing user safety in all decisions
- **Professionalism**: Maintaining high standards of conduct

### Unacceptable Behavior

- Harassment, discrimination, or derogatory comments
- Trolling or deliberately inflammatory comments
- Sharing private information without permission
- Any behavior that compromises user safety

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

1. **Bug Reports**: Report issues you encounter
2. **Feature Suggestions**: Propose new features
3. **Code Contributions**: Submit bug fixes or new features
4. **Documentation**: Improve or add documentation
5. **Testing**: Add or improve test coverage
6. **Crisis Resources**: Update crisis hotline information
7. **Coping Strategies**: Add evidence-based coping techniques

### Before You Start

- Check existing issues and PRs to avoid duplicates
- For major changes, open an issue first to discuss
- Ensure your contribution aligns with project goals
- Review the architecture and coding standards

## Development Setup

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed setup instructions.

Quick start:

```bash
# Clone and setup
git clone https://github.com/WWM-EMRAN/MHSA-Mental-Health-Support-Agent.git
cd MHSA-Mental-Health-Support-Agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest
```

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use type hints for function parameters and returns
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Code Quality Tools

Run these before submitting:

```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/ --max-line-length=100

# Type checking
mypy src/
```

### Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Update relevant .md files for significant changes
- Include examples for new features

Example docstring:

```python
def function_name(param: str) -> Dict[str, any]:
    """Short description of what the function does.
    
    Longer description if needed, explaining the behavior,
    use cases, and any important details.
    
    Args:
        param: Description of the parameter
        
    Returns:
        Description of the return value
        
    Raises:
        ValueError: When and why this is raised
        
    Example:
        >>> result = function_name("test")
        >>> print(result)
        {'key': 'value'}
    """
    pass
```

## Testing Requirements

### Test Coverage

- All new features must include tests
- Aim for >80% code coverage
- Tests must pass before PR can be merged

### Writing Tests

```python
import pytest
from src.agent import MentalHealthAgent

class TestNewFeature:
    """Tests for new feature."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.agent = MentalHealthAgent()
    
    def test_basic_functionality(self):
        """Test basic functionality of new feature."""
        result = self.agent.new_feature()
        assert result is not None
        assert isinstance(result, dict)
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_crisis_detector.py

# With coverage
pytest --cov=src tests/

# Verbose output
pytest -v
```

## Pull Request Process

### 1. Fork and Branch

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/MHSA-Mental-Health-Support-Agent.git
cd MHSA-Mental-Health-Support-Agent

# Create a branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write your code
- Add tests
- Update documentation
- Follow coding standards

### 3. Commit Changes

Use conventional commit messages:

```bash
git add .
git commit -m "feat: add new crisis detection keyword"
git commit -m "fix: correct sentiment analysis edge case"
git commit -m "docs: update API documentation"
```

### 4. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
# Fill out the PR template
```

### 5. PR Review Process

- Automated tests will run
- Maintainers will review your code
- Address any requested changes
- Once approved, PR will be merged

### PR Checklist

Before submitting, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts with main branch
- [ ] PR description explains changes

## Reporting Issues

### Bug Reports

When reporting bugs, include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Detailed steps to reproduce
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: Python version, OS, dependencies
6. **Logs**: Relevant log output or error messages

Example:

```markdown
**Bug Description**
Crisis detection fails for certain phrases

**Steps to Reproduce**
1. Run `python main.py`
2. Enter message: "I'm thinking about ending it all"
3. Crisis not detected

**Expected Behavior**
Should detect crisis and show resources

**Actual Behavior**
No crisis detected, normal response given

**Environment**
- Python 3.9
- macOS 12.0
- MHSA v1.0.0

**Logs**
```
[relevant log output]
```
```

### Feature Requests

When requesting features, include:

1. **Use Case**: Why is this needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Other approaches considered?
4. **Priority**: How important is this?

## Special Guidelines for Mental Health Content

### Crisis Resources

When updating crisis resources:

- Verify all phone numbers and URLs
- Include multiple contact methods (phone, text, chat)
- Provide international resources
- Include specialized resources (LGBTQ+, veterans, etc.)
- Cite sources for information

### Coping Strategies

When adding coping strategies:

- Ensure they are evidence-based
- Cite research or professional guidelines
- Include clear instructions
- Note any contraindications
- Consider accessibility

### Safety First

All contributions must:

- Never remove or disable crisis detection
- Maintain or improve safety features
- Not provide medical advice or diagnoses
- Include appropriate disclaimers
- Prioritize user safety over features

## Review Timeline

- Bug fixes: Reviewed within 2-3 days
- Features: Reviewed within 1 week
- Documentation: Reviewed within 3-5 days

We appreciate your patience!

## Communication

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Pull Requests**: For code contributions

## Recognition

Contributors will be:

- Listed in CONTRIBUTORS.md
- Mentioned in release notes (for significant contributions)
- Credited in relevant documentation

## Questions?

If you have questions about contributing:

1. Check [DEVELOPMENT.md](DEVELOPMENT.md)
2. Search existing issues and discussions
3. Open a new discussion

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions help make mental health support more accessible. Thank you for being part of this important work! 💚

---

Remember: All contributions, no matter how small, are valued and appreciated.
