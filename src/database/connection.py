"""Database connection management."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
from .models import Base

load_dotenv()


class DatabaseConnection:
    """Database connection manager using SQLAlchemy."""
    
    def __init__(self, database_url=None):
        """Initialize database connection.
        
        Args:
            database_url: Database URL. If None, uses DATABASE_URL from env.
        """
        self.database_url = database_url or os.getenv('DATABASE_URL', 'sqlite:///mhsa.db')
        self.engine = None
        self.session_factory = None
        self.Session = None
        
    def connect(self):
        """Establish database connection."""
        self.engine = create_engine(self.database_url, echo=False)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
        
    def create_tables(self):
        """Create all tables in the database."""
        Base.metadata.create_all(self.engine)
        
    def drop_tables(self):
        """Drop all tables from the database."""
        Base.metadata.drop_all(self.engine)
        
    def get_session(self):
        """Get a new database session.
        
        Returns:
            SQLAlchemy session object.
        """
        if self.Session is None:
            self.connect()
        return self.Session()
    
    def close(self):
        """Close the database connection."""
        if self.Session:
            self.Session.remove()
