"""
Base chatbot class with core functionality
"""

from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from .character import Character
from llm.providers import get_llm_provider
from utils.memory import ConversationMemory

class BaseBot(ABC):
    """Base class for all chatbot implementations."""
    
    def __init__(self, character: Character):
        """
        Initialize base bot.
        
        Args:
            character: Character object.
        """
        self.character = character
        self.memory = ConversationMemory()
        self.llm_provider = get_llm_provider()
    
    def chat(self, user_message: str) -> str:
        """
        Process user message and return response.
        
        Args:
            user_message: User's input message.
        
        Returns:
            Bot's response as a string.
        """
        # Add user message to memory
        self.memory.add_message("user", user_message)
        
        # Get conversation context
        messages = self.memory.get_context()
        
        # Get response from LLM
        response = self.llm_provider.generate(
            system_prompt=self.character.get_system_prompt(),
            messages=messages
        )
        
        # Add bot response to memory
        self.memory.add_message("assistant", response)
        
        # Format and return
        return self.format_response(response)
    
    @abstractmethod
    def format_response(self, response: str) -> str:
        """
        Format the response (to be implemented by subclasses).
        
        Args:
            response: Raw response from LLM.
        
        Returns:
            Formatted response.
        """
        pass
    
    def reset_memory(self) -> None:
        """Clear conversation history."""
        self.memory.clear()
    
    def get_character_name(self) -> str:
        """Get the character's name."""
        return self.character.name
    
    def get_memory_summary(self) -> str:
        """Get a summary of the conversation memory."""
        return self.memory.get_summary()