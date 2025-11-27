"""Simple sentiment analysis for mental health conversations."""
from typing import Dict, Union


class SentimentResult(Dict[str, Union[float, str, int]]):
    """Type definition for sentiment analysis results."""
    pass


class SentimentAnalyzer:
    """
    Basic sentiment analyzer for mental health contexts.
    
    Provides simple keyword-based sentiment analysis suitable for
    mental health support conversations.
    """
    
    def __init__(self):
        """Initialize sentiment analyzer with keyword sets."""
        self.positive_keywords = {
            'happy', 'good', 'better', 'great', 'wonderful', 'excellent',
            'hopeful', 'optimistic', 'grateful', 'thankful', 'blessed',
            'excited', 'joyful', 'peaceful', 'calm', 'confident'
        }
        
        self.negative_keywords = {
            'sad', 'depressed', 'anxious', 'worried', 'stressed', 'upset',
            'angry', 'frustrated', 'hopeless', 'helpless', 'worthless',
            'lonely', 'isolated', 'overwhelmed', 'afraid', 'scared',
            'desperate', 'miserable', 'terrible', 'awful', 'horrible'
        }
        
    def analyze(self, text: str) -> SentimentResult:
        """Analyze sentiment of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing:
                - score: Sentiment score (-1 to 1)
                - label: Sentiment label (positive, negative, neutral)
                - positive_count: Number of positive keywords
                - negative_count: Number of negative keywords
        """
        text_lower = text.lower()
        words = text_lower.split()
        
        # Count positive and negative keywords
        positive_count = sum(1 for word in words if word in self.positive_keywords)
        negative_count = sum(1 for word in words if word in self.negative_keywords)
        
        # Calculate score
        total = positive_count + negative_count
        if total == 0:
            score = 0.0
            label = 'neutral'
        else:
            score = (positive_count - negative_count) / total
            if score > 0.2:
                label = 'positive'
            elif score < -0.2:
                label = 'negative'
            else:
                label = 'neutral'
        
        return {
            'score': score,
            'label': label,
            'positive_count': positive_count,
            'negative_count': negative_count
        }
