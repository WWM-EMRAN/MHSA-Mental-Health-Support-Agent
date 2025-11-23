# MHSA API Reference

## Core Classes

### MentalHealthAgent

Main agent class for generating mental health support responses.

#### Constructor

```python
MentalHealthAgent(
    model: str = None,
    temperature: float = None,
    max_tokens: int = None,
    api_key: str = None
)
```

**Parameters:**
- `model` (str, optional): LLM model to use (default: from env or 'gpt-4')
- `temperature` (float, optional): Response randomness 0.0-1.0 (default: 0.7)
- `max_tokens` (int, optional): Maximum tokens in response (default: 1000)
- `api_key` (str, optional): OpenAI API key (default: from env)

**Example:**
```python
from src.agent import MentalHealthAgent

agent = MentalHealthAgent(
    model='gpt-4',
    temperature=0.7,
    max_tokens=1000
)
```

#### Methods

##### generate_response()

```python
generate_response(
    user_message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> Dict[str, any]
```

Generate a response to user's message with crisis detection.

**Parameters:**
- `user_message` (str): User's input message
- `conversation_history` (list, optional): Previous messages

**Returns:**
Dictionary containing:
- `response` (str): Agent's response
- `crisis_detected` (bool): Whether crisis was detected
- `crisis_level` (str): Severity level if crisis detected
- `crisis_keywords` (list): Keywords that triggered detection
- `model_used` (str): Model used for generation

**Example:**
```python
response_data = agent.generate_response(
    user_message="I'm feeling really anxious",
    conversation_history=[
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi! How can I help?"}
    ]
)

print(response_data['response'])
if response_data['crisis_detected']:
    print(f"Crisis Level: {response_data['crisis_level']}")
```

##### get_coping_strategies()

```python
get_coping_strategies(issue_type: str = "general") -> List[str]
```

Get evidence-based coping strategies.

**Parameters:**
- `issue_type` (str): Type of issue - "anxiety", "depression", "stress", "general"

**Returns:**
List of coping strategy strings

**Example:**
```python
strategies = agent.get_coping_strategies("anxiety")
for strategy in strategies:
    print(f"- {strategy}")
```

---

### CrisisDetector

Detects crisis situations in user messages.

#### Constructor

```python
CrisisDetector()
```

**Example:**
```python
from src.agent import CrisisDetector

detector = CrisisDetector()
```

#### Methods

##### detect_crisis()

```python
detect_crisis(message: str) -> Dict[str, any]
```

Detect crisis indicators in a message.

**Parameters:**
- `message` (str): User's message to analyze

**Returns:**
Dictionary containing:
- `crisis_detected` (bool): Whether crisis was detected
- `level` (str): Severity level - "critical", "high", "medium", "none"
- `keywords_found` (list): Crisis keywords found
- `confidence` (float): Confidence score 0.0-1.0

**Example:**
```python
result = detector.detect_crisis("I want to end my life")

if result['crisis_detected']:
    print(f"Level: {result['level']}")
    print(f"Keywords: {result['keywords_found']}")
    print(f"Confidence: {result['confidence']}")
```

##### get_crisis_resources()

```python
get_crisis_resources() -> Dict[str, str]
```

Get crisis resources and hotlines.

**Returns:**
Dictionary of crisis resources with contact information

**Example:**
```python
resources = detector.get_crisis_resources()
print(resources['us_crisis_line'])  # "988 (Suicide & Crisis Lifeline)"
```

---

### ConversationManager

Manages conversation sessions and persistence.

#### Constructor

```python
ConversationManager(db_connection: DatabaseConnection)
```

**Parameters:**
- `db_connection` (DatabaseConnection): Database connection object

**Example:**
```python
from src.database import DatabaseConnection
from src.agent import ConversationManager

db = DatabaseConnection()
db.connect()
manager = ConversationManager(db)
```

#### Methods

##### create_user()

```python
create_user(username: str, email: Optional[str] = None) -> User
```

Create a new user.

**Parameters:**
- `username` (str): Username for the user
- `email` (str, optional): Email address

**Returns:**
User object

**Example:**
```python
user = manager.create_user("john_doe", "john@example.com")
print(f"Created user: {user.id}")
```

##### get_or_create_user()

```python
get_or_create_user(username: str, email: Optional[str] = None) -> User
```

Get existing user or create new one.

**Returns:**
User object

##### start_conversation()

```python
start_conversation(user_id: int, title: Optional[str] = None) -> Conversation
```

Start a new conversation session.

**Parameters:**
- `user_id` (int): ID of the user
- `title` (str, optional): Title for the conversation

**Returns:**
Conversation object

**Example:**
```python
conversation = manager.start_conversation(
    user_id=user.id,
    title="Evening check-in"
)
```

##### add_message()

```python
add_message(
    conversation_id: int,
    role: str,
    content: str,
    sentiment_score: Optional[float] = None,
    crisis_detected: bool = False
) -> Message
```

Add a message to a conversation.

**Parameters:**
- `conversation_id` (int): ID of the conversation
- `role` (str): Message role - 'user' or 'assistant'
- `content` (str): Message content
- `sentiment_score` (float, optional): Sentiment score -1.0 to 1.0
- `crisis_detected` (bool): Whether crisis was detected

**Returns:**
Message object

**Example:**
```python
message = manager.add_message(
    conversation_id=conversation.id,
    role='user',
    content='I need help',
    sentiment_score=-0.5
)
```

##### get_conversation_history()

```python
get_conversation_history(
    conversation_id: int,
    limit: Optional[int] = None
) -> List[Dict[str, str]]
```

Get conversation history formatted for the agent.

**Parameters:**
- `conversation_id` (int): ID of the conversation
- `limit` (int, optional): Maximum number of messages

**Returns:**
List of message dictionaries with 'role' and 'content'

**Example:**
```python
history = manager.get_conversation_history(conversation.id, limit=10)
# Returns: [{"role": "user", "content": "..."}, ...]
```

##### end_conversation()

```python
end_conversation(conversation_id: int) -> None
```

Mark a conversation as ended.

---

### DatabaseConnection

Manages database connections and sessions.

#### Constructor

```python
DatabaseConnection(database_url: str = None)
```

**Parameters:**
- `database_url` (str, optional): Database URL (default: from env or SQLite)

**Example:**
```python
from src.database import DatabaseConnection

# SQLite
db = DatabaseConnection('sqlite:///mhsa.db')

# PostgreSQL
db = DatabaseConnection('postgresql://user:pass@localhost/mhsa')
```

#### Methods

##### connect()

```python
connect() -> None
```

Establish database connection.

##### create_tables()

```python
create_tables() -> None
```

Create all database tables.

##### get_session()

```python
get_session() -> Session
```

Get a new database session.

**Returns:**
SQLAlchemy session object

##### close()

```python
close() -> None
```

Close database connection.

**Complete Example:**
```python
db = DatabaseConnection()
db.connect()
db.create_tables()

session = db.get_session()
# Use session...
session.close()

db.close()
```

---

### SentimentAnalyzer

Basic sentiment analysis for mental health contexts.

#### Constructor

```python
SentimentAnalyzer()
```

#### Methods

##### analyze()

```python
analyze(text: str) -> Dict[str, any]
```

Analyze sentiment of text.

**Parameters:**
- `text` (str): Text to analyze

**Returns:**
Dictionary containing:
- `score` (float): Sentiment score -1.0 to 1.0
- `label` (str): Sentiment label - "positive", "negative", "neutral"
- `positive_count` (int): Number of positive keywords
- `negative_count` (int): Number of negative keywords

**Example:**
```python
from src.utils import SentimentAnalyzer

analyzer = SentimentAnalyzer()
result = analyzer.analyze("I'm feeling happy and hopeful today")

print(f"Score: {result['score']}")  # 1.0
print(f"Label: {result['label']}")  # "positive"
```

---

## Database Models

### User Model

```python
class User(Base):
    id: int              # Primary key
    username: str        # Unique username
    email: str           # Email (nullable)
    created_at: datetime # Creation timestamp
    last_active: datetime # Last activity
    is_active: bool      # Active status
    conversations: List[Conversation]  # Relationship
```

### Conversation Model

```python
class Conversation(Base):
    id: int              # Primary key
    user_id: int         # Foreign key to User
    title: str           # Conversation title
    started_at: datetime # Start timestamp
    ended_at: datetime   # End timestamp (nullable)
    is_active: bool      # Active status
    sentiment_score: float # Overall sentiment (nullable)
    crisis_detected: bool  # Crisis flag
    messages: List[Message]  # Relationship
```

### Message Model

```python
class Message(Base):
    id: int              # Primary key
    conversation_id: int # Foreign key to Conversation
    role: str            # 'user' or 'assistant'
    content: str         # Message content
    timestamp: datetime  # Message timestamp
    sentiment_score: float # Sentiment score (nullable)
    crisis_keywords_detected: bool  # Crisis flag
```

---

## Usage Examples

### Complete Conversation Flow

```python
from src.agent import MentalHealthAgent, ConversationManager
from src.database import DatabaseConnection
from src.utils import SentimentAnalyzer

# Setup
db = DatabaseConnection()
db.connect()
db.create_tables()

manager = ConversationManager(db)
agent = MentalHealthAgent(model='gpt-4')
sentiment = SentimentAnalyzer()

# Create user and start conversation
user = manager.get_or_create_user("john_doe")
conversation = manager.start_conversation(user.id)

# User message
user_message = "I'm feeling really anxious about work"
sentiment_result = sentiment.analyze(user_message)

# Save user message
manager.add_message(
    conversation.id,
    'user',
    user_message,
    sentiment_score=sentiment_result['score']
)

# Get agent response
history = manager.get_conversation_history(conversation.id)
response_data = agent.generate_response(user_message, history)

# Save agent response
manager.add_message(
    conversation.id,
    'assistant',
    response_data['response'],
    crisis_detected=response_data['crisis_detected']
)

print(response_data['response'])

# End conversation
manager.end_conversation(conversation.id)
db.close()
```

### Crisis Detection Example

```python
from src.agent import CrisisDetector

detector = CrisisDetector()

messages = [
    "I'm feeling sad",
    "I'm feeling hopeless and worthless",
    "I want to kill myself"
]

for msg in messages:
    result = detector.detect_crisis(msg)
    print(f"Message: {msg}")
    print(f"Crisis: {result['crisis_detected']}")
    print(f"Level: {result['level']}")
    print()
```

---

## Error Handling

All methods may raise exceptions:

- `ValueError`: Invalid parameters
- `ConnectionError`: Database connection issues
- `APIError`: LLM API failures
- `Exception`: Other errors

Always wrap calls in try-except blocks:

```python
try:
    response = agent.generate_response(message)
except Exception as e:
    print(f"Error: {e}")
    # Handle error appropriately
```
