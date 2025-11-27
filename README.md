# MHSA - Mental Health Support Agent 🧠💚

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**MHSA (Mental Health Support Agent)** is an empathetic AI-powered conversational agent designed to provide mental health support, crisis detection, and coping strategies. This is a capstone project for the Google 5-day Intensive Agentic AI course.

## 🌟 Features

- **Empathetic Conversation**: Natural, supportive dialogue powered by advanced language models
- **Crisis Detection**: Automatic detection of crisis situations with immediate resource provision
- **Conversation Management**: Persistent conversation history with database storage
- **Coping Strategies**: Evidence-based coping techniques for various mental health concerns
- **Sentiment Analysis**: Basic sentiment tracking throughout conversations
- **Safety First**: Built-in safety protocols and crisis resource management
- **Multi-Model Support**: Compatible with OpenAI GPT models (GPT-4, GPT-3.5-turbo)

## ⚠️ Important Disclaimer

**MHSA is NOT a replacement for professional mental health services.** This agent:
- Does NOT diagnose mental health conditions
- Does NOT prescribe medication or treatment
- Does NOT replace therapy or counseling
- Should NOT be used as the sole resource in crisis situations

**If you are in immediate danger, please call emergency services (911 in the US) or the 988 Suicide & Crisis Lifeline.**

## 🏗️ Architecture

```
MHSA/
├── src/
│   ├── agent/              # Core agent logic
│   │   ├── mental_health_agent.py    # Main agent implementation
│   │   ├── crisis_detector.py        # Crisis detection system
│   │   └── conversation_manager.py   # Conversation management
│   ├── database/           # Database models and connection
│   │   ├── models.py                 # SQLAlchemy models
│   │   └── connection.py             # Database connection manager
│   └── utils/              # Utility modules
│       ├── logger.py                 # Logging configuration
│       └── sentiment_analyzer.py     # Sentiment analysis
├── resources/
│   ├── prompts/            # System prompts
│   └── crisis_resources/   # Crisis hotlines and coping strategies
├── docs/                   # Documentation
├── tests/                  # Test suite
├── config/                 # Configuration files
└── main.py                 # CLI application entry point
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for GPT models)
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/WWM-EMRAN/MHSA-Mental-Health-Support-Agent.git
cd MHSA-Mental-Health-Support-Agent
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. **Run the application**
```bash
python main.py
```

## 🔧 Configuration

Edit the `.env` file to configure the application:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration
DEFAULT_MODEL=gpt-4              # or gpt-3.5-turbo
TEMPERATURE=0.7                  # 0.0 to 1.0
MAX_TOKENS=1000

# Database Configuration
DATABASE_URL=sqlite:///mhsa.db   # or postgresql://...

# Application Configuration
DEBUG=False
LOG_LEVEL=INFO                   # DEBUG, INFO, WARNING, ERROR

# Safety Configuration
ENABLE_CRISIS_DETECTION=True
```

## 💻 Usage

### CLI Interface

Run the interactive command-line interface:

```bash
python main.py
```

**Commands:**
- Type your message to chat with the agent
- `strategies` - Get coping strategies for different situations
- `crisis` - View crisis resources and hotlines
- `quit` or `exit` - End the session

### Python API

Use MHSA programmatically in your Python code:

```python
from src.agent import MentalHealthAgent
from src.database import DatabaseConnection
from src.agent import ConversationManager

# Initialize agent
agent = MentalHealthAgent(model='gpt-4', temperature=0.7)

# Generate response
response_data = agent.generate_response(
    user_message="I'm feeling really anxious today",
    conversation_history=[]
)

print(response_data['response'])
if response_data['crisis_detected']:
    print("Crisis detected! Level:", response_data['crisis_level'])
```

## 📊 Database Schema

MHSA uses SQLAlchemy with SQLite (default) or PostgreSQL:

**Tables:**
- `users` - User accounts and profiles
- `conversations` - Conversation sessions
- `messages` - Individual messages in conversations
- `session_manager` - Active session tracking

## 🛡️ Safety Features

### Crisis Detection

The agent automatically detects crisis situations using keyword analysis:

- **Critical Level**: Suicidal ideation, self-harm
- **High Level**: Self-harm mentions, crisis keywords
- **Medium Level**: Multiple concerning indicators

When a crisis is detected, the agent:
1. Acknowledges the seriousness
2. Provides immediate crisis resources
3. Encourages contacting professional help
4. Logs the incident for follow-up

### Crisis Resources

Built-in crisis resources include:
- 988 Suicide & Crisis Lifeline (US)
- Crisis Text Line (Text HOME to 741741)
- International crisis resources
- LGBTQ+ specific support (Trevor Project)
- Veterans Crisis Line
- Emergency services information

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/
```

## 📚 Resources

### Coping Strategies

The agent provides evidence-based coping strategies for:
- Anxiety management (breathing exercises, grounding techniques)
- Depression support (behavioral activation, self-compassion)
- Stress reduction (mindfulness, time management)
- Sleep hygiene
- General wellness

### Documentation

- [Architecture Documentation](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Crisis Protocol](docs/CRISIS_PROTOCOL.md)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](docs/CONTRIBUTING.md) before submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google 5-day Intensive Agentic AI Course
- OpenAI for GPT models
- Mental health professionals who provided guidance on best practices
- Crisis hotline organizations providing vital services

## 📞 Crisis Resources

**If you or someone you know is in crisis:**

- **US**: Call or text 988 (Suicide & Crisis Lifeline)
- **US**: Text HOME to 741741 (Crisis Text Line)
- **International**: Visit https://www.iasp.info/resources/Crisis_Centres/
- **Emergency**: Call 911 (US) or local emergency services

## 🔗 Links

- [GitHub Repository](https://github.com/WWM-EMRAN/MHSA-Mental-Health-Support-Agent)
- [Documentation](docs/)
- [Issue Tracker](https://github.com/WWM-EMRAN/MHSA-Mental-Health-Support-Agent/issues)

---

**Remember**: Seeking help is a sign of strength, not weakness. You are not alone. 💚
