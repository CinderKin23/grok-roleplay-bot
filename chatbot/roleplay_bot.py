"""
Roleplay Bot - Custom character roleplay engine
"""

from typing import Optional, List, Dict
from chatbot.base_bot import BaseBot
import os


class RoleplayBot(BaseBot):
    """Bot that takes on custom character personalities for roleplay"""
    
    def __init__(self, character: Dict):
        """
        Initialize roleplay bot with character definition
        
        Args:
            character: Dictionary with character properties
        """
        self.character = character
        self.character_name = character.get('name', 'Unknown')
        self.character_role = character.get('role', '')
        
        # Build system prompt from character
        system_prompt = self._build_system_prompt(character)
        super().__init__(system_prompt=system_prompt)
        
        self.model = os.getenv('MODEL', 'gpt-4-turbo')
    
    def _build_system_prompt(self, character: Dict) -> str:
        """Build system prompt from character definition"""
        if 'prompt_template' in character:
            return character['prompt_template']
        
        # Build prompt from individual fields
        name = character.get('name', 'Unknown')
        role = character.get('role', '')
        personality = character.get('personality', '')
        background = character.get('background', '')
        speaking_style = character.get('speaking_style', 'natural')
        
        prompt = f"""You are {name}, a {role}.

Personality: {personality}
Background: {background}
Speaking Style: {speaking_style}

Respond authentically as this character would. Be engaging and immersive. Keep responses to 2-3 sentences usually, unless context requires more."""
        
        return prompt
    
    def get_response(self, user_input: str, context: Optional[List[Dict]] = None, is_greeting: bool = False) -> str:
        """
        Get character's response
        
        Args:
            user_input: User's message
            context: Conversation history
            is_greeting: If True, generate an initial greeting instead of responding
            
        Returns:
            Character's response
        """
        # Build message list
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add context if available
        if context:
            for msg in context:
                role = msg.get("role", "user")
                # Map character names to assistant role for context
                if role == self.character_name:
                    role = "assistant"
                messages.append({
                    "role": role,
                    "content": msg.get("content", "")
                })
        
        # Add current message
        if is_greeting:
            greeting_prompt = f"Begin a roleplay scene. You are {self.character_name}. Start with an engaging greeting or introduction that establishes your character. Be concise (1-2 sentences)."
            messages.append({"role": "user", "content": greeting_prompt})
        else:
            if user_input.strip():
                messages.append({"role": "user", "content": user_input})
            else:
                return f"{self.character_name}: ..."
        
        # Get response from LLM
        if self.llm_provider == 'openai':
            return self._call_openai(messages, model=self.model, temperature=0.8)
        elif self.llm_provider == 'anthropic':
            return self._call_anthropic(messages, temperature=0.8)
        else:
            return self._fallback_response()
    
    def _fallback_response(self) -> str:
        """Provide fallback response when LLM unavailable""" 
        return f"{self.character_name}: *pauses thoughtfully* I'm afraid my connection to the world is momentarily disrupted. Please bear with me.",