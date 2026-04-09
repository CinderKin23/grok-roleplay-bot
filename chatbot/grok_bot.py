"""
Grok-level chatbot implementation
"""

from typing import Optional, List, Dict, Any
from .character import Character, GROK_CHARACTER
from .base_bot import BaseBot

class GrokBot(BaseBot):
    """Grok-level chatbot with sarcasm and honesty."""
    
    def __init__(self, character: Optional[Character] = None):
        """
        Initialize Grok Bot.
        
        Args:
            character: Optional Character object. Defaults to Grok.
        """
        if character is None:
            character = GROK_CHARACTER
        
        super().__init__(character)
    
    def format_response(self, response: str) -> str:
        """Format response with Grok's style."""
        return response