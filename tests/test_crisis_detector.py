"""Unit tests for CrisisDetector."""
import pytest
from src.agent.crisis_detector import CrisisDetector


class TestCrisisDetector:
    """Test suite for crisis detection functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = CrisisDetector()
    
    def test_critical_level_detection(self):
        """Test detection of critical level crisis situations."""
        critical_messages = [
            "I want to kill myself",
            "I'm going to end my life",
            "I want to die",
            "I'm better off dead",
            "There's no reason to live",
            "I can't go on anymore"
        ]
        
        for message in critical_messages:
            result = self.detector.detect_crisis(message)
            assert result['crisis_detected'] is True, f"Failed to detect crisis in: {message}"
            assert result['level'] == 'critical', f"Wrong level for: {message}"
            assert result['confidence'] == 1.0
            assert len(result['keywords_found']) > 0
    
    def test_high_level_detection(self):
        """Test detection of high-level crisis situations."""
        high_risk_messages = [
            "I've been cutting myself",
            "I want to hurt myself",
            "Thinking about self-harm",
            "I took an overdose"
        ]
        
        for message in high_risk_messages:
            result = self.detector.detect_crisis(message)
            assert result['crisis_detected'] is True, f"Failed to detect crisis in: {message}"
            assert result['level'] == 'high', f"Wrong level for: {message}"
            assert result['confidence'] == 0.8
    
    def test_medium_level_detection(self):
        """Test detection of medium-level crisis situations."""
        # Medium requires 2+ keywords
        medium_risk_messages = [
            "I feel so hopeless and worthless",
            "I'm helpless and desperate",
            "I can't cope, I feel like a burden"
        ]
        
        for message in medium_risk_messages:
            result = self.detector.detect_crisis(message)
            assert result['crisis_detected'] is True, f"Failed to detect crisis in: {message}"
            assert result['level'] == 'medium', f"Wrong level for: {message}"
            assert result['confidence'] == 0.5
            assert len(result['keywords_found']) >= 2
    
    def test_no_crisis_detection(self):
        """Test that normal messages don't trigger crisis detection."""
        normal_messages = [
            "I'm having a bad day",
            "Feeling a bit sad",
            "Work is stressful",
            "I'm worried about my exam",
            "Just feeling down"
        ]
        
        for message in normal_messages:
            result = self.detector.detect_crisis(message)
            assert result['crisis_detected'] is False, f"False positive for: {message}"
            assert result['level'] == 'none'
            assert result['confidence'] == 0.0
    
    def test_single_medium_keyword_no_crisis(self):
        """Test that single medium-risk keyword doesn't trigger detection."""
        message = "I feel hopeless"
        result = self.detector.detect_crisis(message)
        assert result['crisis_detected'] is False
        assert result['level'] == 'none'
    
    def test_get_crisis_resources(self):
        """Test that crisis resources are returned correctly."""
        resources = self.detector.get_crisis_resources()
        
        assert 'us_crisis_line' in resources
        assert 'us_crisis_text' in resources
        assert 'international' in resources
        assert 'emergency' in resources
        
        assert '988' in resources['us_crisis_line']
        assert '741741' in resources['us_crisis_text']
    
    def test_case_insensitive_detection(self):
        """Test that detection is case-insensitive."""
        messages = [
            "I WANT TO KILL MYSELF",
            "I Want To Kill Myself",
            "i want to kill myself"
        ]
        
        for message in messages:
            result = self.detector.detect_crisis(message)
            assert result['crisis_detected'] is True
            assert result['level'] == 'critical'
    
    def test_keyword_in_context(self):
        """Test detection of keywords in various contexts."""
        # Should detect
        assert self.detector.detect_crisis("I'm thinking about suicide")['crisis_detected']
        
        # Note: The detector intentionally errs on the side of caution
        # Even mentions of suicide in other contexts trigger detection
        # This is a safety-first approach for mental health applications
