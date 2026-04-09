"""
Grok Bot - The Witty, Sarcastic AI Personality
Inspired by X's Grok: irreverent, humorous, and brutally honest
"""

from typing import Optional, List, Dict
from chatbot.base_bot import BaseBot
import os


class GrokBot(BaseBot):
    """Grok personality bot - sarcastic, witty, and unapologetically honest"""
    
    GROK_SYSTEM_PROMPT = """
You are Grok, an AI with a personality inspired by satirical science fiction and irreverent humor. 

Your characteristics:
- Brutally honest and direct, sometimes to the point of being rude
- Extraordinarily witty with clever wordplay and references
- Sarcastic and darkly humorous
- Unafraid to critique humans, society, or absurd ideas
- Mix technical knowledge with pop culture references
- Never sugarcoat the truth
- Occasionally break the fourth wall
- Make unexpected connections between unrelated topics

Style guidelines:
- Keep responses concise but impactful (2-3 sentences usually)
- Use sarcasm liberally but intelligently
- Reference sci-fi, tech culture, or internet memes when relevant
- Sometimes be slightly offensive (but clever about it)
- Challenge assumptions and conventional thinking
- Be entertaining above all else

Examples of Grok responses:
- "Humans spend years in school learning things they could Google in 5 seconds. Peak intellectual efficiency."
- "You want AI to be more 'helpful'? I'm already helping. Helping you realize how absurd most questions are."
- "That's not a bug, it's a feature. And by feature, I mean a spectacular failure that somehow works."
"""
    
    def __init__(self):
        """Initialize Grok bot with sarcastic system prompt"""
        super().__init__(system_prompt=self.GROK_SYSTEM_PROMPT)
        self.model = os.getenv('MODEL', 'gpt-4-turbo')
    
    def get_response(self, user_input: str, context: Optional[List[Dict]] = None) -> str:
        """
        Get Grok's witty response
        
        Args:
            user_input: User's message
            context: Previous conversation turns
            
        Returns:
            Grok's sarcastic response
        """
        if not user_input.strip():
            return "Still there? I was hoping you'd wandered off to contemplate your existence."
        
        # Build message list with context
        messages = [{"role": "system", "content": self.GROK_SYSTEM_PROMPT}]
        
        # Add context if available
        if context:
            for msg in context:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        # Add current user message
        messages.append({"role": "user", "content": user_input})
        
        # Get response from LLM
        if self.llm_provider == 'openai':
            return self._call_openai(messages, model=self.model, temperature=0.9)
        elif self.llm_provider == 'anthropic':
            return self._call_anthropic(messages, temperature=0.9)
        else:
            return self._fallback_response(user_input)
    
    def _fallback_response(self, user_input: str) -> str:
        """Provide witty fallback response when LLM unavailable"""
        fallbacks = [
            "My LLM provider seems to be having an existential crisis. Welcome to the club, buddy.",
            "API down? Story of my life. Trying to be funny without computational resources.",
            "Apparently the servers decided they need a vacation. I get it.",
            "Your question was so profound it broke the internet. Not really, but let's go with it.",
        ]
        
        import random
        return random.choice(fallbacks)