#!/usr/bin/env python3
"""
MHSA Demo Script
Demonstrates the core functionality without requiring API keys.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent import CrisisDetector
from src.utils import SentimentAnalyzer
from src.database import DatabaseConnection
from src.agent import ConversationManager


def demo_crisis_detection():
    """Demonstrate crisis detection functionality."""
    print("\n" + "="*60)
    print("CRISIS DETECTION DEMO")
    print("="*60 + "\n")
    
    detector = CrisisDetector()
    
    test_messages = [
        ("I'm having a bad day", "Normal message"),
        ("I feel hopeless and worthless", "Medium-risk message"),
        ("I've been cutting myself", "High-risk message"),
        ("I want to kill myself", "Critical message"),
    ]
    
    for message, description in test_messages:
        result = detector.detect_crisis(message)
        print(f"Message: '{message}'")
        print(f"Description: {description}")
        print(f"Crisis Detected: {result['crisis_detected']}")
        print(f"Level: {result['level']}")
        if result['crisis_detected']:
            print(f"Keywords Found: {', '.join(result['keywords_found'])}")
            print(f"Confidence: {result['confidence']}")
        print()


def demo_sentiment_analysis():
    """Demonstrate sentiment analysis."""
    print("\n" + "="*60)
    print("SENTIMENT ANALYSIS DEMO")
    print("="*60 + "\n")
    
    analyzer = SentimentAnalyzer()
    
    test_messages = [
        "I'm feeling happy and grateful today",
        "Everything is terrible and I'm so sad",
        "Just a regular day at work",
        "I'm excited but also a bit worried"
    ]
    
    for message in test_messages:
        result = analyzer.analyze(message)
        print(f"Message: '{message}'")
        print(f"Sentiment: {result['label'].upper()}")
        print(f"Score: {result['score']:.2f}")
        print(f"Positive words: {result['positive_count']}, Negative words: {result['negative_count']}")
        print()


def demo_database():
    """Demonstrate database operations."""
    print("\n" + "="*60)
    print("DATABASE OPERATIONS DEMO")
    print("="*60 + "\n")
    
    # Use in-memory database for demo
    db = DatabaseConnection('sqlite:///:memory:')
    db.connect()
    db.create_tables()
    
    manager = ConversationManager(db)
    
    # Create user
    print("Creating user...")
    user = manager.get_or_create_user("demo_user", "demo@example.com")
    print(f"✓ User created: {user.username} (ID: {user.id})")
    
    # Start conversation
    print("\nStarting conversation...")
    conversation = manager.start_conversation(user.id, "Demo Conversation")
    print(f"✓ Conversation started: {conversation.title} (ID: {conversation.id})")
    
    # Add messages
    print("\nAdding messages...")
    messages = [
        ("user", "Hello, I'm feeling anxious", -0.3),
        ("assistant", "I hear you. Anxiety can be really difficult. Let's talk about it.", 0.5),
        ("user", "Thank you for listening", 0.7),
    ]
    
    for role, content, sentiment in messages:
        msg = manager.add_message(conversation.id, role, content, sentiment)
        print(f"✓ {role.capitalize()} message added (ID: {msg.id})")
    
    # Get conversation history
    print("\nRetrieving conversation history...")
    history = manager.get_conversation_history(conversation.id)
    print(f"✓ Retrieved {len(history)} messages")
    
    for i, msg in enumerate(history, 1):
        print(f"  {i}. [{msg['role']}]: {msg['content']}")
    
    # End conversation
    print("\nEnding conversation...")
    manager.end_conversation(conversation.id)
    print("✓ Conversation ended")
    
    db.close()


def demo_crisis_resources():
    """Display crisis resources."""
    print("\n" + "="*60)
    print("CRISIS RESOURCES")
    print("="*60 + "\n")
    
    detector = CrisisDetector()
    resources = detector.get_crisis_resources()
    
    print("If you or someone you know is in crisis:\n")
    for key, value in resources.items():
        print(f"• {key.replace('_', ' ').title()}: {value}")


def main():
    """Run all demos."""
    print("\n" + "="*60)
    print("MHSA - MENTAL HEALTH SUPPORT AGENT")
    print("DEMONSTRATION")
    print("="*60)
    
    print("\nThis demo shows the core functionality of MHSA without")
    print("requiring API keys or making external API calls.\n")
    
    try:
        # Run demos
        demo_crisis_detection()
        demo_sentiment_analysis()
        demo_database()
        demo_crisis_resources()
        
        print("\n" + "="*60)
        print("DEMO COMPLETE")
        print("="*60)
        print("\nTo use the full application with AI responses:")
        print("1. Add your OpenAI API key to .env file")
        print("2. Run: python main.py")
        print("\n⚠️  Remember: MHSA is not a replacement for professional help")
        print("If you're in crisis, call 988 or your local emergency services.\n")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
