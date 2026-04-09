"""
Base Bot Class - Core conversational engine
"""

import os
from abc import ABC, abstractmethod
from typing import Optional, Dict, List


class BaseBot(ABC):
    """Abstract base class for all bot implementations"""
    
    def __init__(self, system_prompt: str = ""):
        """
        Initialize the base bot
        
        Args:
            system_prompt: System-level instructions for the bot
        """
        self.system_prompt = system_prompt
        self.llm_provider = self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize LLM provider based on environment"""
        provider = os.getenv('LLM_PROVIDER', 'openai').lower()
        
        if provider == 'openai':
            try:
                import openai
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    raise ValueError("OPENAI_API_KEY environment variable not set")
                openai.api_key = api_key
                return 'openai'
            except ImportError:
                print("⚠️  OpenAI library not found. Install with: pip install openai")
                return None
        
        elif provider == 'anthropic':
            try:
                import anthropic
                return 'anthropic'
            except ImportError:
                print("⚠️  Anthropic library not found. Install with: pip install anthropic")
                return None
        
        return None
    
    @abstractmethod
    def get_response(self, user_input: str, context: Optional[List[Dict]] = None) -> str:
        """Get bot response to user input
        
        Args:
            user_input: User's message
            context: Conversation history context
            
        Returns:
            Bot's response string
        """
        pass
    
    def _call_openai(self, messages: List[Dict], model: str = "gpt-4-turbo", temperature: float = 0.7) -> str:
        """Call OpenAI API"""
        try:
            import openai
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"
    
    def _call_anthropic(self, messages: List[Dict], model: str = "claude-3-opus-20240229", temperature: float = 0.7) -> str:
        """Call Anthropic API"""
        try:
            import anthropic
            client = anthropic.Anthropic()
            response = client.messages.create(
                model=model,
                max_tokens=500,
                temperature=temperature,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            return f"Error calling Anthropic: {str(e)}"
    
    def _generate_local_response(self, prompt: str) -> str:
        """Generate response using local model (Ollama, etc.)
        Placeholder for local model integration"""
        return "Local model integration not yet configured. Please set up Ollama or similar."