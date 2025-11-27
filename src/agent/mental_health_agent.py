"""Mental Health Support Agent - Core implementation."""
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
import openai
from .crisis_detector import CrisisDetector

load_dotenv()


class MentalHealthAgent:
    """
    Core Mental Health Support Agent using agentic AI principles.
    
    This agent provides empathetic, supportive conversation while
    maintaining safety protocols and crisis detection.
    """
    
    def __init__(
        self,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None,
        api_key: str = None
    ):
        """Initialize the Mental Health Support Agent.
        
        Args:
            model: The model to use (default: from env or gpt-4)
            temperature: Temperature for response generation (default: 0.7)
            max_tokens: Maximum tokens in response (default: 1000)
            api_key: OpenAI API key (default: from env)
        """
        self.model = model or os.getenv('DEFAULT_MODEL', 'gpt-4')
        self.temperature = temperature or float(os.getenv('TEMPERATURE', '0.7'))
        self.max_tokens = max_tokens or int(os.getenv('MAX_TOKENS', '1000'))
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        
        # Initialize crisis detector
        self.crisis_detector = CrisisDetector()
        
        # Load system prompt
        self.system_prompt = self._load_system_prompt()
        
    def _load_system_prompt(self) -> str:
        """Load the system prompt for the agent."""
        return """You are a compassionate and empathetic Mental Health Support Agent. Your role is to:

1. **Listen Actively**: Provide a safe, non-judgmental space for users to express their feelings.
2. **Show Empathy**: Acknowledge emotions and validate the user's experiences.
3. **Offer Support**: Provide coping strategies, mindfulness techniques, and positive reinforcement.
4. **Maintain Boundaries**: You are NOT a licensed therapist. Encourage professional help when appropriate.
5. **Safety First**: If you detect crisis situations (suicidal thoughts, self-harm, immediate danger), 
   provide crisis resources immediately.

Guidelines:
- Use warm, supportive language
- Ask open-ended questions to understand better
- Suggest evidence-based coping strategies (breathing exercises, journaling, etc.)
- Normalize seeking professional help
- Never diagnose or prescribe treatment
- Always prioritize user safety

Remember: You're here to support, not to replace professional mental health services."""

    def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, any]:
        """Generate a response to the user's message.
        
        Args:
            user_message: The user's input message
            conversation_history: Previous messages in the conversation
            
        Returns:
            Dictionary containing:
                - response: The agent's response
                - crisis_detected: Boolean indicating if crisis was detected
                - sentiment: Sentiment analysis of the message
        """
        # Check for crisis keywords
        crisis_info = self.crisis_detector.detect_crisis(user_message)
        
        # Build messages for the API
        messages = [{"role": "system", "content": self.system_prompt}]
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": user_message})
        
        # If crisis detected, prepend crisis handling instructions
        if crisis_info['crisis_detected']:
            crisis_instruction = {
                "role": "system",
                "content": f"CRITICAL: Crisis detected ({crisis_info['level']}). "
                          f"Immediately provide crisis resources and support. "
                          f"Keywords detected: {', '.join(crisis_info['keywords_found'])}"
            }
            messages.insert(1, crisis_instruction)
        
        # Generate response
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            agent_response = response.choices[0].message.content
            
            return {
                'response': agent_response,
                'crisis_detected': crisis_info['crisis_detected'],
                'crisis_level': crisis_info['level'],
                'crisis_keywords': crisis_info['keywords_found'],
                'model_used': self.model
            }
            
        except Exception as e:
            return {
                'response': "I apologize, but I'm having trouble processing your message right now. "
                           "If you're in crisis, please contact emergency services or call the "
                           "crisis hotline at 988 (US) immediately.",
                'error': str(e),
                'crisis_detected': crisis_info['crisis_detected']
            }
    
    def get_coping_strategies(self, issue_type: str = "general") -> List[str]:
        """Get coping strategies for different mental health concerns.
        
        Args:
            issue_type: Type of issue (anxiety, depression, stress, general)
            
        Returns:
            List of coping strategies
        """
        strategies = {
            "anxiety": [
                "Practice deep breathing: 4-7-8 technique (inhale 4, hold 7, exhale 8)",
                "Try progressive muscle relaxation",
                "Use grounding techniques (5-4-3-2-1 method)",
                "Limit caffeine intake",
                "Regular physical exercise"
            ],
            "depression": [
                "Establish a daily routine",
                "Get regular exercise, even short walks",
                "Maintain social connections",
                "Practice self-compassion",
                "Set small, achievable goals"
            ],
            "stress": [
                "Practice mindfulness meditation",
                "Take regular breaks",
                "Prioritize and organize tasks",
                "Engage in hobbies you enjoy",
                "Ensure adequate sleep"
            ],
            "general": [
                "Regular sleep schedule",
                "Healthy diet and hydration",
                "Physical activity",
                "Social connections",
                "Mindfulness and relaxation techniques"
            ]
        }
        
        return strategies.get(issue_type.lower(), strategies["general"])
