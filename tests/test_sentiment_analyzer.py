"""Unit tests for SentimentAnalyzer."""
import pytest
from src.utils.sentiment_analyzer import SentimentAnalyzer


class TestSentimentAnalyzer:
    """Test suite for sentiment analysis functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = SentimentAnalyzer()
    
    def test_positive_sentiment(self):
        """Test detection of positive sentiment."""
        positive_messages = [
            "I'm feeling happy and great today",
            "Things are wonderful and I'm grateful",
            "Feeling hopeful and optimistic"
        ]
        
        for message in positive_messages:
            result = self.analyzer.analyze(message)
            assert result['label'] == 'positive', f"Failed for: {message}"
            assert result['score'] > 0
            assert result['positive_count'] > 0
    
    def test_negative_sentiment(self):
        """Test detection of negative sentiment."""
        negative_messages = [
            "I'm feeling sad and depressed",
            "Everything is awful and horrible",
            "Feeling anxious and worried"
        ]
        
        for message in negative_messages:
            result = self.analyzer.analyze(message)
            assert result['label'] == 'negative', f"Failed for: {message}"
            assert result['score'] < 0
            assert result['negative_count'] > 0
    
    def test_neutral_sentiment(self):
        """Test detection of neutral sentiment."""
        neutral_messages = [
            "I went to the store today",
            "The weather is okay",
            "Just a regular day"
        ]
        
        for message in neutral_messages:
            result = self.analyzer.analyze(message)
            assert result['label'] == 'neutral', f"Failed for: {message}"
            assert result['score'] == 0.0
    
    def test_mixed_sentiment(self):
        """Test messages with both positive and negative words."""
        message = "I'm happy but also worried"
        result = self.analyzer.analyze(message)
        
        assert result['positive_count'] == 1
        assert result['negative_count'] == 1
        assert result['label'] == 'neutral'  # Should balance out
    
    def test_score_range(self):
        """Test that scores are within valid range."""
        messages = [
            "extremely happy wonderful great",
            "terrible awful horrible sad",
            "just a normal day"
        ]
        
        for message in messages:
            result = self.analyzer.analyze(message)
            assert -1.0 <= result['score'] <= 1.0
    
    def test_empty_message(self):
        """Test handling of empty message."""
        result = self.analyzer.analyze("")
        assert result['label'] == 'neutral'
        assert result['score'] == 0.0
        assert result['positive_count'] == 0
        assert result['negative_count'] == 0
