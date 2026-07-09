#!/usr/bin/env python
"""
Simple launcher for the AI NPC Game
Automatically uses API key from config.py
"""

print("\n" + "="*70)
print("  🎮 AI NPC GAME - NPCs with Soul")
print("="*70)

# Import the API key from config
from npc_game.config import GROQ_API_KEY

if not GROQ_API_KEY:
    print("\n❌ ERROR: No API key found in config.py!")
    print("\nPlease add your Groq API key to: npc_game/config.py")
    print("Set: GROQ_API_KEY = 'your-key-here'")
    exit(1)

print(f"\n✓ API Key loaded: {GROQ_API_KEY[:15]}...")

# Import and create game
from npc_game.game import create_demo_game

print("✓ Creating game world...")
game = create_demo_game(groq_api_key=GROQ_API_KEY)

print("✓ Game ready!\n")

# Start the interactive loop
game.run_interactive_loop()
