"""Conversation management for maintaining context and history."""
from typing import List, Dict, Optional
from datetime import datetime
from src.database import DatabaseConnection, User, Conversation, Message


class ConversationManager:
    """
    Manages conversation sessions and history.
    
    Handles storing, retrieving, and managing conversation context
    for users interacting with the mental health agent.
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        """Initialize conversation manager.
        
        Args:
            db_connection: Database connection object
        """
        self.db = db_connection
        
    def create_user(self, username: str, email: Optional[str] = None) -> User:
        """Create a new user.
        
        Args:
            username: Username for the user
            email: Optional email address
            
        Returns:
            User object
        """
        session = self.db.get_session()
        try:
            user = User(username=username, email=email)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()
    
    def get_or_create_user(self, username: str, email: Optional[str] = None) -> User:
        """Get existing user or create new one.
        
        Args:
            username: Username to look for
            email: Optional email
            
        Returns:
            User object
        """
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                user = User(username=username, email=email)
                session.add(user)
                session.commit()
                session.refresh(user)
            return user
        finally:
            session.close()
    
    def start_conversation(self, user_id: int, title: Optional[str] = None) -> Conversation:
        """Start a new conversation session.
        
        Args:
            user_id: ID of the user
            title: Optional title for the conversation
            
        Returns:
            Conversation object
        """
        session = self.db.get_session()
        try:
            conversation = Conversation(
                user_id=user_id,
                title=title or f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            return conversation
        finally:
            session.close()
    
    def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
        sentiment_score: Optional[float] = None,
        crisis_detected: bool = False
    ) -> Message:
        """Add a message to a conversation.
        
        Args:
            conversation_id: ID of the conversation
            role: Message role ('user' or 'assistant')
            content: Message content
            sentiment_score: Optional sentiment score
            crisis_detected: Whether crisis was detected
            
        Returns:
            Message object
        """
        session = self.db.get_session()
        try:
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
                sentiment_score=sentiment_score,
                crisis_keywords_detected=crisis_detected
            )
            session.add(message)
            session.commit()
            session.refresh(message)
            return message
        finally:
            session.close()
    
    def get_conversation_history(
        self,
        conversation_id: int,
        limit: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """Get conversation history in format suitable for the agent.
        
        Args:
            conversation_id: ID of the conversation
            limit: Optional limit on number of messages
            
        Returns:
            List of message dictionaries with 'role' and 'content'
        """
        session = self.db.get_session()
        try:
            query = session.query(Message).filter_by(conversation_id=conversation_id)
            query = query.order_by(Message.timestamp.asc())
            
            if limit:
                query = query.limit(limit)
            
            messages = query.all()
            
            return [
                {'role': msg.role, 'content': msg.content}
                for msg in messages
            ]
        finally:
            session.close()
    
    def end_conversation(self, conversation_id: int) -> None:
        """Mark a conversation as ended.
        
        Args:
            conversation_id: ID of the conversation
        """
        session = self.db.get_session()
        try:
            conversation = session.query(Conversation).filter_by(id=conversation_id).first()
            if conversation:
                conversation.is_active = False
                conversation.ended_at = datetime.utcnow()
                session.commit()
        finally:
            session.close()
    
    def get_user_conversations(self, user_id: int) -> List[Conversation]:
        """Get all conversations for a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            List of Conversation objects
        """
        session = self.db.get_session()
        try:
            conversations = session.query(Conversation)\
                .filter_by(user_id=user_id)\
                .order_by(Conversation.started_at.desc())\
                .all()
            return conversations
        finally:
            session.close()
