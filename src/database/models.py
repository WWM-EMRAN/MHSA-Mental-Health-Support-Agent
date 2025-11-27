"""Database models for MHSA."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    """User model for storing user information."""
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=func.now())
    last_active = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    conversations = relationship('Conversation', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Conversation(Base):
    """Conversation model for storing conversation sessions."""
    
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=True)
    started_at = Column(DateTime, default=func.now())
    ended_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    sentiment_score = Column(Float, nullable=True)  # Overall sentiment of conversation
    crisis_detected = Column(Boolean, default=False)
    
    # Relationships
    user = relationship('User', back_populates='conversations')
    messages = relationship('Message', back_populates='conversation', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, started_at={self.started_at})>"


class Message(Base):
    """Message model for storing individual messages in conversations."""
    
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    sentiment_score = Column(Float, nullable=True)
    crisis_keywords_detected = Column(Boolean, default=False)
    
    # Relationships
    conversation = relationship('Conversation', back_populates='messages')
    
    def __repr__(self):
        return f"<Message(id={self.id}, conversation_id={self.conversation_id}, role='{self.role}')>"


class SessionManager(Base):
    """Session manager for tracking active sessions and metadata."""
    
    __tablename__ = 'session_manager'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    session_metadata = Column(Text, nullable=True)  # JSON string for additional data
    
    def __repr__(self):
        return f"<SessionManager(id={self.id}, session_id='{self.session_id}')>"
