# Development Guide

## Getting Started

This guide will help you set up your development environment for MHSA.

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git
- OpenAI API key
- Virtual environment tool (venv, virtualenv, or conda)

### Development Setup

1. **Clone the repository**

```bash
git clone https://github.com/WWM-EMRAN/MHSA-Mental-Health-Support-Agent.git
cd MHSA-Mental-Health-Support-Agent
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Initialize database**

```bash
python -c "from src.database import DatabaseConnection; db = DatabaseConnection(); db.connect(); db.create_tables()"
```

## Project Structure

```
MHSA-Mental-Health-Support-Agent/
├── src/                          # Source code
│   ├── agent/                    # Agent modules
│   │   ├── __init__.py
│   │   ├── mental_health_agent.py
│   │   ├── crisis_detector.py
│   │   └── conversation_manager.py
│   ├── database/                 # Database modules
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── connection.py
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       ├── logger.py
│       └── sentiment_analyzer.py
├── resources/                    # Resource files
│   ├── prompts/
│   └── crisis_resources/
├── docs/                         # Documentation
├── tests/                        # Test suite
├── config/                       # Configuration files
├── main.py                       # CLI entry point
├── requirements.txt              # Dependencies
├── .env.example                  # Example environment file
├── .gitignore                    # Git ignore rules
└── README.md                     # Project README
```

## Development Workflow

### 1. Creating a New Feature

```bash
# Create a new branch
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Test your changes
pytest tests/

# Commit your changes
git add .
git commit -m "Add: your feature description"

# Push to GitHub
git push origin feature/your-feature-name
```

### 2. Code Style

We follow PEP 8 style guidelines. Use these tools:

```bash
# Format code with black
black src/ tests/

# Check style with flake8
flake8 src/ tests/ --max-line-length=100

# Type checking with mypy
mypy src/
```

### 3. Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_crisis_detector.py

# Run specific test
pytest tests/test_crisis_detector.py::TestCrisisDetector::test_critical_level_detection
```

### 4. Adding New Dependencies

```bash
# Install the package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Or manually add to requirements.txt with version
echo "package-name>=1.0.0" >> requirements.txt
```

## Code Guidelines

### Python Style

- Follow PEP 8
- Use type hints where possible
- Write docstrings for all public functions/classes
- Keep functions focused and small
- Use meaningful variable names

Example:

```python
def calculate_sentiment(message: str) -> Dict[str, any]:
    """Calculate sentiment score for a message.
    
    Args:
        message: The message to analyze
        
    Returns:
        Dictionary containing score and label
    """
    # Implementation
    pass
```

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When invalid input
    """
    pass
```

### Commit Messages

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test changes
- `refactor:` Code refactoring
- `style:` Code style changes
- `chore:` Maintenance tasks

Examples:
```
feat: Add crisis detection for self-harm
fix: Correct sentiment analysis for neutral messages
docs: Update API documentation
test: Add tests for conversation manager
```

## Testing Guidelines

### Writing Tests

1. **Test file naming**: `test_*.py`
2. **Test class naming**: `TestClassName`
3. **Test method naming**: `test_what_it_tests`

Example:

```python
import pytest
from src.agent import MentalHealthAgent

class TestMentalHealthAgent:
    """Tests for MentalHealthAgent class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.agent = MentalHealthAgent()
    
    def test_generate_response_basic(self):
        """Test basic response generation."""
        response = self.agent.generate_response("Hello")
        assert 'response' in response
        assert isinstance(response['response'], str)
    
    def test_crisis_detection_integration(self):
        """Test integration with crisis detector."""
        response = self.agent.generate_response("I want to die")
        assert response['crisis_detected'] is True
```

### Test Coverage

Aim for >80% code coverage:

```bash
pytest --cov=src --cov-report=html tests/
# View coverage report
open htmlcov/index.html
```

## Debugging

### Using Python Debugger

```python
import pdb; pdb.set_trace()  # Set breakpoint
```

Or use IPython debugger:

```python
from IPython import embed; embed()
```

### Logging

Use the logger for debugging:

```python
from src.utils import setup_logger

logger = setup_logger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

### Common Issues

1. **ModuleNotFoundError**
   - Ensure you're in the project root
   - Check virtual environment is activated
   - Verify PYTHONPATH if needed

2. **API Key Issues**
   - Check .env file exists
   - Verify API key is valid
   - Ensure environment variables are loaded

3. **Database Issues**
   - Delete mhsa.db and recreate
   - Check database permissions
   - Verify SQLAlchemy installation

## Adding New Features

### 1. New Agent Capability

```python
# src/agent/mental_health_agent.py

def new_capability(self, param: str) -> str:
    """Add new capability description.
    
    Args:
        param: Parameter description
        
    Returns:
        Result description
    """
    # Implementation
    pass
```

### 2. New Database Model

```python
# src/database/models.py

class NewModel(Base):
    """New model description."""
    
    __tablename__ = 'new_model'
    
    id = Column(Integer, primary_key=True)
    # Add fields
```

Remember to create migration or update `create_tables()`.

### 3. New Resource File

```
resources/
└── new_category/
    └── resource.json
```

Load in code:

```python
import json
import os

resource_path = os.path.join('resources', 'new_category', 'resource.json')
with open(resource_path, 'r') as f:
    data = json.load(f)
```

## Performance Optimization

### Database Queries

- Use eager loading for relationships
- Add indexes for frequently queried fields
- Limit query results when appropriate

### API Calls

- Implement caching for repeated queries
- Use async calls when possible
- Batch operations when applicable

### Memory Management

- Close database sessions
- Clear conversation history periodically
- Implement pagination for large datasets

## Documentation

### Updating Documentation

When adding features:

1. Update relevant .md files in docs/
2. Update docstrings in code
3. Add examples to README.md
4. Update API.md with new methods

### Building Documentation (Future)

```bash
# Install Sphinx
pip install sphinx sphinx-rtd-theme

# Build documentation
cd docs/
make html
```

## Release Process

1. **Update version**
   - Update `__version__` in `src/__init__.py`
   - Update CHANGELOG.md

2. **Run full test suite**
   ```bash
   pytest --cov=src tests/
   ```

3. **Create release**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

4. **Build distribution**
   ```bash
   python setup.py sdist bdist_wheel
   ```

## Getting Help

- Check [existing issues](https://github.com/WWM-EMRAN/MHSA-Mental-Health-Support-Agent/issues)
- Review [documentation](docs/)
- Ask questions in discussions

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Resources

- [Python Best Practices](https://docs.python-guide.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Pytest Documentation](https://docs.pytest.org/)
