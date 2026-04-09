"""
Conversation Memory Management
"""

from typing import List, Dict, Optional
from collections import deque
from datetime import datetime


class ConversationMemory:
    """Manages conversation history and context"""
    
    def __init__(self, max_history: int = 10):
        """Initialize conversation memory
        
        Args:
            max_history: Maximum number of turns to keep in memory
        """
        self.max_history = max_history
        self.messages: deque = deque(maxlen=max_history)
        self.start_time = datetime.now()    
    def add_message(self, role: str, content: str) -> None:
        """Add message to memory
        
        Args:
            role: Who sent the message (user, bot, character name, etc.)
            content: Message content
        """
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_context(self, num_turns: Optional[int] = None) -> List[Dict]:
        """Get conversation context for LLM
        
        Args:
            num_turns: Number of previous turns to include (None = all)
            
        Returns:
            List of messages for context
        """
        if num_turns and num_turns < len(self.messages):
            return list(self.messages)[-num_turns:]
        return list(self.messages)
    
    def get_summary(self) -> str:
        """Get brief summary of conversation"""
        return f"Conversation with {len(self.messages)} messages, started at {self.start_time.strftime('%H:%M:%S')}"
    
    def clear(self) -> None:
        """Clear all conversation history"""
        self.messages.clear()
        self.start_time = datetime.now()
    
    def get_last_message(self, role: Optional[str] = None) -> Optional[Dict]:
        """Get last message, optionally filtered by role
        
        Args:
            role: Optional role to filter by
            
        Returns:
            Last message or None
        """
        if not self.messages:
            return None
        
        if role:
            for msg in reversed(self.messages):
                if msg["role"] == role:
                    return msg
            return None
        
        return self.messages[-1]
    
    def export_conversation(self) -> str:
        """Export conversation as formatted text"""
        lines = [f"=== Conversation ({self.get_summary()}) ===\n"]
        for msg in self.messages:
            role = msg["role"].upper()
            content = msg["content"]
            lines.append(f"{role}: {content}\n")
        return "".join(lines)