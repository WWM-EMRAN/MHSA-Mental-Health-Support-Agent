"""Unit tests for database functionality."""
import pytest
from datetime import datetime
from src.database import DatabaseConnection, User, Conversation, Message


class TestDatabase:
    """Test suite for database operations."""
    
    def setup_method(self):
        """Set up test fixtures with in-memory database."""
        self.db = DatabaseConnection('sqlite:///:memory:')
        self.db.connect()
        self.db.create_tables()
    
    def teardown_method(self):
        """Clean up after tests."""
        self.db.close()
    
    def test_create_user(self):
        """Test user creation."""
        session = self.db.get_session()
        
        user = User(username='testuser', email='test@example.com')
        session.add(user)
        session.commit()
        
        # Verify user was created
        retrieved_user = session.query(User).filter_by(username='testuser').first()
        assert retrieved_user is not None
        assert retrieved_user.username == 'testuser'
        assert retrieved_user.email == 'test@example.com'
        assert retrieved_user.is_active is True
        
        session.close()
    
    def test_create_conversation(self):
        """Test conversation creation."""
        session = self.db.get_session()
        
        # Create user first
        user = User(username='testuser')
        session.add(user)
        session.commit()
        
        # Create conversation
        conversation = Conversation(
            user_id=user.id,
            title='Test Conversation'
        )
        session.add(conversation)
        session.commit()
        
        # Verify conversation
        retrieved_conv = session.query(Conversation).filter_by(user_id=user.id).first()
        assert retrieved_conv is not None
        assert retrieved_conv.title == 'Test Conversation'
        assert retrieved_conv.is_active is True
        
        session.close()
    
    def test_create_message(self):
        """Test message creation."""
        session = self.db.get_session()
        
        # Create user and conversation
        user = User(username='testuser')
        session.add(user)
        session.commit()
        
        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()
        
        # Create message
        message = Message(
            conversation_id=conversation.id,
            role='user',
            content='Test message',
            sentiment_score=0.5
        )
        session.add(message)
        session.commit()
        
        # Verify message
        retrieved_msg = session.query(Message).filter_by(conversation_id=conversation.id).first()
        assert retrieved_msg is not None
        assert retrieved_msg.content == 'Test message'
        assert retrieved_msg.role == 'user'
        assert retrieved_msg.sentiment_score == 0.5
        
        session.close()
    
    def test_user_conversation_relationship(self):
        """Test relationship between user and conversations."""
        session = self.db.get_session()
        
        # Create user
        user = User(username='testuser')
        session.add(user)
        session.commit()
        
        # Create multiple conversations
        for i in range(3):
            conv = Conversation(user_id=user.id, title=f'Conversation {i}')
            session.add(conv)
        session.commit()
        
        # Verify relationship
        retrieved_user = session.query(User).filter_by(username='testuser').first()
        assert len(retrieved_user.conversations) == 3
        
        session.close()
    
    def test_conversation_message_relationship(self):
        """Test relationship between conversation and messages."""
        session = self.db.get_session()
        
        # Create user and conversation
        user = User(username='testuser')
        session.add(user)
        session.commit()
        
        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()
        
        # Create multiple messages
        for i in range(5):
            msg = Message(
                conversation_id=conversation.id,
                role='user' if i % 2 == 0 else 'assistant',
                content=f'Message {i}'
            )
            session.add(msg)
        session.commit()
        
        # Verify relationship
        retrieved_conv = session.query(Conversation).first()
        assert len(retrieved_conv.messages) == 5
        
        session.close()
    
    def test_crisis_flag_storage(self):
        """Test storage of crisis detection flags."""
        session = self.db.get_session()
        
        # Create user and conversation
        user = User(username='testuser')
        session.add(user)
        session.commit()
        
        conversation = Conversation(user_id=user.id, crisis_detected=True)
        session.add(conversation)
        session.commit()
        
        # Create message with crisis flag
        message = Message(
            conversation_id=conversation.id,
            role='user',
            content='Crisis message',
            crisis_keywords_detected=True
        )
        session.add(message)
        session.commit()
        
        # Verify flags
        retrieved_conv = session.query(Conversation).first()
        assert retrieved_conv.crisis_detected is True
        
        retrieved_msg = session.query(Message).first()
        assert retrieved_msg.crisis_keywords_detected is True
        
        session.close()
