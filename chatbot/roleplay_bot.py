"""
Roleplay bot implementation for custom characters
"""

from typing import Optional, List, Dict, Any
from .character import Character
from .base_bot import BaseBot

class RoleplayBot(BaseBot):
    """Advanced roleplay bot supporting custom characters."""
    
    def __init__(self, character: Character):
        """
        Initialize Roleplay Bot.
        
        Args:
            character: Character object to roleplay as.
        """
        if not isinstance(character, Character):
            raise TypeError("character must be a Character instance")
        
        super().__init__(character)
    
    def change_character(self, character: Character) -> None:
        """
        Switch to a different character.
        
        Args:
            character: New Character object.
        """
        self.character = character
        self.reset_memory()
    
    def format_response(self, response: str) -> str:
        """Format response with the character's style."""
        return response
