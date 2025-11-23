"""Crisis detection system for identifying urgent mental health situations."""
from typing import Dict, List, Set
import re


class CrisisDetector:
    """
    Detects crisis situations in user messages.
    
    This system identifies keywords and patterns that may indicate
    suicidal thoughts, self-harm, or other crisis situations.
    """
    
    def __init__(self):
        """Initialize the crisis detector with keyword sets."""
        # Critical crisis keywords
        self.critical_keywords = {
            'suicide', 'suicidal', 'kill myself', 'end my life',
            'want to die', 'better off dead', 'no reason to live',
            'can\'t go on', 'ending it all'
        }
        
        # High-risk keywords
        self.high_risk_keywords = {
            'self harm', 'self-harm', 'cut myself', 'cutting',
            'hurt myself', 'harm myself', 'overdose', 'pills',
            'die', 'death', 'suicide plan'
        }
        
        # Medium-risk keywords
        self.medium_risk_keywords = {
            'hopeless', 'helpless', 'worthless', 'burden',
            'give up', 'can\'t cope', 'no point', 'empty inside',
            'numb', 'desperate'
        }
        
    def detect_crisis(self, message: str) -> Dict[str, any]:
        """Detect crisis indicators in a message.
        
        Args:
            message: User's message to analyze
            
        Returns:
            Dictionary containing:
                - crisis_detected: Boolean indicating if crisis was detected
                - level: Severity level (critical, high, medium, none)
                - keywords_found: List of crisis keywords found
                - confidence: Confidence score (0-1)
        """
        message_lower = message.lower()
        
        # Check for critical keywords
        critical_found = self._find_keywords(message_lower, self.critical_keywords)
        if critical_found:
            return {
                'crisis_detected': True,
                'level': 'critical',
                'keywords_found': critical_found,
                'confidence': 1.0
            }
        
        # Check for high-risk keywords
        high_risk_found = self._find_keywords(message_lower, self.high_risk_keywords)
        if high_risk_found:
            return {
                'crisis_detected': True,
                'level': 'high',
                'keywords_found': high_risk_found,
                'confidence': 0.8
            }
        
        # Check for medium-risk keywords (need multiple matches)
        medium_risk_found = self._find_keywords(message_lower, self.medium_risk_keywords)
        if len(medium_risk_found) >= 2:
            return {
                'crisis_detected': True,
                'level': 'medium',
                'keywords_found': medium_risk_found,
                'confidence': 0.5
            }
        
        return {
            'crisis_detected': False,
            'level': 'none',
            'keywords_found': [],
            'confidence': 0.0
        }
    
    def _find_keywords(self, message: str, keywords: Set[str]) -> List[str]:
        """Find which keywords from a set are present in the message.
        
        Args:
            message: Lowercase message to search
            keywords: Set of keywords to look for
            
        Returns:
            List of found keywords
        """
        found = []
        for keyword in keywords:
            # Use word boundary for better matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, message):
                found.append(keyword)
        return found
    
    def get_crisis_resources(self) -> Dict[str, str]:
        """Get crisis resources and hotlines.
        
        Returns:
            Dictionary of crisis resources
        """
        return {
            'us_crisis_line': '988 (Suicide & Crisis Lifeline)',
            'us_crisis_text': 'Text HOME to 741741 (Crisis Text Line)',
            'international': '+1-800-273-8255',
            'emergency': '911 (US) or local emergency services',
            'online_chat': 'https://988lifeline.org/chat',
            'trevor_project': '1-866-488-7386 (LGBTQ+ Youth)',
            'veterans_crisis': '988 then press 1, or text 838255'
        }
