# MHSA Architecture Documentation

## Overview

The Mental Health Support Agent (MHSA) is built using a modular, layered architecture that separates concerns and enables scalability and maintainability.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  (CLI Application / Future: Web Interface, API)             │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    Application Layer                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Main.py   │  │  CLI App     │  │  Future: API │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                      Agent Layer                             │
│  ┌────────────────────┐  ┌─────────────────┐               │
│  │ MentalHealthAgent  │  │ CrisisDetector  │               │
│  └────────────────────┘  └─────────────────┘               │
│  ┌────────────────────┐  ┌─────────────────┐               │
│  │ ConversationMgr    │  │ PromptManager   │               │
│  └────────────────────┘  └─────────────────┘               │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    Service Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ OpenAI API   │  │ Sentiment    │  │ Logger       │      │
│  │ Integration  │  │ Analyzer     │  │ Service      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                     Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ SQLAlchemy   │  │ Database     │  │ Resource     │      │
│  │ Models       │  │ Connection   │  │ Files        │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Agent Layer

#### MentalHealthAgent
**Purpose**: Core conversational agent providing mental health support

**Responsibilities**:
- Generate empathetic responses using LLM (GPT-4)
- Maintain conversation context
- Apply system prompts and safety guidelines
- Coordinate with crisis detector
- Provide coping strategies

**Key Methods**:
- `generate_response()`: Main method for response generation
- `get_coping_strategies()`: Retrieve evidence-based coping techniques
- `_load_system_prompt()`: Load and manage system prompts

#### CrisisDetector
**Purpose**: Identify crisis situations in real-time

**Responsibilities**:
- Keyword-based crisis detection
- Risk level assessment (critical, high, medium)
- Crisis resource provision
- Safety protocol activation

**Detection Levels**:
- **Critical**: Immediate suicide risk, self-harm
- **High**: Self-harm mentions, concerning patterns
- **Medium**: Multiple distress indicators

#### ConversationManager
**Purpose**: Manage conversation persistence and state

**Responsibilities**:
- User session management
- Conversation history tracking
- Message storage and retrieval
- Database operations coordination

### 2. Database Layer

#### Models
- **User**: User profiles and metadata
- **Conversation**: Conversation sessions
- **Message**: Individual messages with metadata
- **SessionManager**: Active session tracking

#### DatabaseConnection
**Purpose**: Centralized database connection management

**Features**:
- Connection pooling
- Session management
- Table creation/migration support
- SQLite and PostgreSQL support

### 3. Utilities Layer

#### Logger
**Purpose**: Centralized logging system

**Features**:
- Console and file logging
- Configurable log levels
- Structured log format
- Daily log rotation

#### SentimentAnalyzer
**Purpose**: Basic sentiment analysis

**Features**:
- Keyword-based sentiment scoring
- Positive/negative/neutral classification
- Conversation mood tracking

## Data Flow

### Typical Conversation Flow

```
1. User Input
   ↓
2. CLI App receives message
   ↓
3. Sentiment Analysis performed
   ↓
4. Message saved to database (User role)
   ↓
5. Crisis Detection check
   ↓
6. Context loaded from conversation history
   ↓
7. MentalHealthAgent generates response
   ↓
8. Response saved to database (Assistant role)
   ↓
9. Crisis resources shown (if needed)
   ↓
10. Response displayed to user
```

### Crisis Detection Flow

```
User Message
   ↓
CrisisDetector.detect_crisis()
   ↓
Keyword Matching
   ├─ Critical Keywords → Level: CRITICAL
   ├─ High-Risk Keywords → Level: HIGH
   └─ Medium Keywords (2+) → Level: MEDIUM
   ↓
Return Detection Result
   ↓
If Crisis Detected:
   ├─ Add crisis instruction to prompt
   ├─ Agent generates supportive response
   ├─ Display crisis resources
   └─ Log incident
```

## Design Patterns

### 1. Repository Pattern
Database operations are abstracted through managers (ConversationManager) that handle all data access logic.

### 2. Strategy Pattern
Crisis detection uses different strategies based on severity levels.

### 3. Singleton Pattern
DatabaseConnection and Logger use singleton-like behavior for centralized management.

### 4. Factory Pattern
Agent initialization with configurable parameters (model, temperature, etc.).

## Scalability Considerations

### Current Implementation
- SQLite for simple deployment
- Single-threaded CLI application
- In-memory conversation context

### Future Enhancements
- PostgreSQL for production
- Web API with FastAPI/Flask
- Redis for session caching
- Horizontal scaling with load balancing
- Asynchronous message processing
- Multi-model support (Anthropic Claude, etc.)

## Security Considerations

### Data Privacy
- User data stored locally by default
- No data transmitted except to LLM API
- Configurable data retention policies

### API Key Management
- Environment variables for secrets
- No hardcoded credentials
- `.env` files excluded from version control

### Crisis Safety
- Automatic crisis detection
- Mandatory resource provision
- Logging for follow-up

## Configuration Management

### Environment Variables
All configuration through `.env` file:
- API credentials
- Model parameters
- Database connection
- Logging levels
- Feature flags

### Resource Files
- System prompts (resources/prompts/)
- Crisis resources (resources/crisis_resources/)
- Coping strategies (resources/crisis_resources/)

## Testing Strategy

### Unit Tests
- Agent response generation
- Crisis detection accuracy
- Database operations
- Sentiment analysis

### Integration Tests
- End-to-end conversation flow
- Database persistence
- API integration

### Manual Testing
- Crisis scenario validation
- User experience testing
- Safety protocol verification

## Performance Considerations

### Response Time
- Average: 2-5 seconds (LLM API dependent)
- Crisis detection: <100ms
- Database operations: <50ms

### Optimization Opportunities
- Caching frequent responses
- Async API calls
- Connection pooling
- Query optimization

## Deployment Options

### Local Deployment
```bash
python main.py
```

### Docker Deployment (Future)
```bash
docker build -t mhsa .
docker run -p 5000:5000 mhsa
```

### Cloud Deployment (Future)
- AWS Lambda for serverless
- Google Cloud Run for containers
- Azure App Service

## Monitoring and Logging

### Logging Levels
- **DEBUG**: Development information
- **INFO**: Normal operations
- **WARNING**: Attention needed
- **ERROR**: Error conditions
- **CRITICAL**: System failures

### Metrics to Monitor
- Conversation count
- Crisis detection rate
- Response latency
- Error rates
- User satisfaction (future)

## Future Architecture Enhancements

### Phase 2: Web Interface
- React/Vue.js frontend
- RESTful API backend
- WebSocket for real-time chat

### Phase 3: Advanced Features
- Multi-modal support (voice, video)
- ML-based sentiment analysis
- Personalized recommendations
- Therapist dashboard
- Analytics and reporting

### Phase 4: Scale
- Microservices architecture
- Event-driven processing
- Global CDN deployment
- Multi-language support
