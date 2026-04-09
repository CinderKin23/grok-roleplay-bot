#!/usr/bin/env python3
"""
Grok Roleplay Bot - Main Entry Point
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from chatbot import GrokBot, RoleplayBot
from config.settings import get_settings

# Load environment variables
load_dotenv()

def print_banner():
    """Print the Grok bot banner."""
    banner = """
    ╔════════════════════════════════════════╗
    ║     GROK ROLEPLAY BOT v1.0              ║
    ║     Sarcasm Level: Maximum             ║
    ╚════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main entry point."""
    print_banner()
    
    settings = get_settings()
    
    # Choose bot mode
    print("\n[1] Grok Mode (Pure sarcasm)")
    print("[2] Custom Character Roleplay")
    print("[3] Multi-Character Scene")
    
    choice = input("\nSelect mode (1-3): ").strip()
    
    if choice == "1":
        bot = GrokBot()
        print("\nGrok: 'Oh great, another human. Prepare for actual honesty.'\n")
    elif choice == "2":
        name = input("Character name: ").strip()
        personality = input("Personality description: ").strip()
        background = input("Background (optional): ").strip() or None
        
        from chatbot.character import Character
        character = Character(name=name, personality=personality, background=background)
        bot = RoleplayBot(character=character)
        print(f"\n{name}: *appears before you*\n")
    else:
        print("Invalid choice. Defaulting to Grok mode.")
        bot = GrokBot()
    
    # Chat loop
    print("Type 'quit' to exit, 'reset' to clear history\n")
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "quit":
                print("\nGrok: 'Finally, peace and quiet.'")
                break
            
            if user_input.lower() == "reset":
                bot.reset_memory()
                print("[Conversation history cleared]\n")
                continue
            
            response = bot.chat(user_input)
            print(f"\n{bot.get_character_name()}: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGrok: 'Rude much?'")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    main()