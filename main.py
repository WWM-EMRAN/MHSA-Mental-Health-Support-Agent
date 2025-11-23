#!/usr/bin/env python3
"""
MHSA - Mental Health Support Agent
Main application entry point for CLI interface.
"""
import os
import sys
from typing import Optional
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent import MentalHealthAgent, ConversationManager
from src.database import DatabaseConnection
from src.utils import setup_logger, SentimentAnalyzer

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger()


class MHSACliApp:
    """CLI Application for Mental Health Support Agent."""
    
    def __init__(self):
        """Initialize the CLI application."""
        self.agent = None
        self.db = None
        self.conversation_manager = None
        self.sentiment_analyzer = SentimentAnalyzer()
        self.current_user = None
        self.current_conversation = None
        
    def initialize(self):
        """Initialize database and agent."""
        try:
            # Initialize database
            self.db = DatabaseConnection()
            self.db.connect()
            self.db.create_tables()
            logger.info("Database initialized successfully")
            
            # Initialize conversation manager
            self.conversation_manager = ConversationManager(self.db)
            
            # Initialize agent
            self.agent = MentalHealthAgent()
            logger.info("Mental Health Agent initialized successfully")
            
            return True
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            print(f"{Fore.RED}Failed to initialize: {e}")
            return False
    
    def print_welcome(self):
        """Print welcome message."""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}    Mental Health Support Agent (MHSA)")
        print(f"{Fore.CYAN}    Your compassionate AI companion")
        print(f"{Fore.CYAN}{'='*60}\n")
        print(f"{Fore.YELLOW}Welcome! I'm here to listen and support you.")
        print(f"{Fore.YELLOW}This is a safe space to share your feelings.\n")
        print(f"{Fore.WHITE}Commands:")
        print(f"  - Type your message to chat")
        print(f"  - Type 'strategies' for coping strategies")
        print(f"  - Type 'crisis' for emergency resources")
        print(f"  - Type 'quit' or 'exit' to end the session\n")
        print(f"{Fore.RED}⚠️  IMPORTANT: If you're in immediate danger, call emergency services (911)")
        print(f"{Fore.RED}   or the crisis hotline at 988 (US)\n")
    
    def print_crisis_resources(self):
        """Print crisis resources."""
        resources = self.agent.crisis_detector.get_crisis_resources()
        print(f"\n{Fore.RED}{'='*60}")
        print(f"{Fore.RED}    CRISIS RESOURCES")
        print(f"{Fore.RED}{'='*60}\n")
        print(f"{Fore.YELLOW}If you're experiencing a mental health crisis:\n")
        for key, value in resources.items():
            print(f"{Fore.WHITE}  • {key.replace('_', ' ').title()}: {Fore.CYAN}{value}")
        print(f"\n{Fore.YELLOW}You are not alone. Help is available 24/7.\n")
    
    def start_session(self, username: str):
        """Start a conversation session.
        
        Args:
            username: Username for the session
        """
        # Get or create user
        self.current_user = self.conversation_manager.get_or_create_user(username)
        
        # Start conversation
        self.current_conversation = self.conversation_manager.start_conversation(
            self.current_user.id
        )
        
        logger.info(f"Started session for user {username}")
    
    def chat_loop(self):
        """Main chat loop."""
        conversation_history = []
        
        while True:
            # Get user input
            try:
                user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n")
                break
            
            if not user_input:
                continue
            
            # Check for commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(f"\n{Fore.CYAN}Agent: {Fore.WHITE}Take care of yourself. "
                      f"Remember, seeking help is a sign of strength, not weakness. "
                      f"I hope our conversation was helpful.\n")
                break
            
            if user_input.lower() == 'crisis':
                self.print_crisis_resources()
                continue
            
            if user_input.lower() == 'strategies':
                print(f"\n{Fore.CYAN}Agent: {Fore.WHITE}Here are some coping strategies:\n")
                strategies = self.agent.get_coping_strategies()
                for i, strategy in enumerate(strategies, 1):
                    print(f"  {i}. {strategy}")
                print()
                continue
            
            # Analyze sentiment
            sentiment = self.sentiment_analyzer.analyze(user_input)
            
            # Save user message
            self.conversation_manager.add_message(
                conversation_id=self.current_conversation.id,
                role='user',
                content=user_input,
                sentiment_score=sentiment['score']
            )
            
            # Generate response
            response_data = self.agent.generate_response(
                user_input,
                conversation_history
            )
            
            # Check for crisis
            if response_data.get('crisis_detected'):
                print(f"\n{Fore.RED}⚠️  CRISIS ALERT DETECTED ⚠️{Style.RESET_ALL}\n")
                self.print_crisis_resources()
            
            # Print agent response
            agent_response = response_data['response']
            print(f"\n{Fore.CYAN}Agent: {Fore.WHITE}{agent_response}\n")
            
            # Save agent message
            self.conversation_manager.add_message(
                conversation_id=self.current_conversation.id,
                role='assistant',
                content=agent_response,
                crisis_detected=response_data.get('crisis_detected', False)
            )
            
            # Update conversation history
            conversation_history.append({'role': 'user', 'content': user_input})
            conversation_history.append({'role': 'assistant', 'content': agent_response})
            
            # Keep only last 10 messages for context (to avoid token limits)
            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]
    
    def end_session(self):
        """End the current session."""
        if self.current_conversation:
            self.conversation_manager.end_conversation(self.current_conversation.id)
            logger.info(f"Ended conversation {self.current_conversation.id}")
        
        if self.db:
            self.db.close()
    
    def run(self):
        """Run the CLI application."""
        # Initialize
        if not self.initialize():
            sys.exit(1)
        
        # Print welcome
        self.print_welcome()
        
        # Get username
        username = input(f"{Fore.YELLOW}Please enter your name (or a nickname): {Style.RESET_ALL}").strip()
        if not username:
            username = "Anonymous"
        
        print(f"\n{Fore.CYAN}Hello {username}! How are you feeling today?\n")
        
        # Start session
        self.start_session(username)
        
        # Main chat loop
        try:
            self.chat_loop()
        finally:
            self.end_session()


def main():
    """Main entry point."""
    app = MHSACliApp()
    app.run()


if __name__ == '__main__':
    main()
