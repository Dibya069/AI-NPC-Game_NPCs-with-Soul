"""
Main entry point for the AI NPC Game
"""

import os
from npc_game.game import create_demo_game
from npc_game.config import GROQ_API_KEY


def main():
    """Run the game"""
    print("\n🎮 Starting AI NPC Game...")

    # Get API key from config or environment
    api_key = GROQ_API_KEY or os.getenv('GROQ_API_KEY')

    if not api_key:
        print("\n⚠️  Warning: GROQ_API_KEY not found!")
        print("The game will run but NPCs won't have AI-powered responses.")
        print("\nTo enable AI responses:")
        print("  1. Get a free API key from: https://console.groq.com/")
        print("  2. Add it to npc_game/config.py: GROQ_API_KEY = 'your-key-here'")
        print("  3. Or set environment: export GROQ_API_KEY='your-key-here'")
        print("  4. Restart the game\n")

        choice = input("Continue without AI? (y/n): ").strip().lower()
        if choice != 'y':
            print("Exiting...")
            return
    else:
        print(f"✓ API Key loaded: {api_key[:15]}...")

    # Create and run the game
    game = create_demo_game(groq_api_key=api_key)
    game.run_interactive_loop()


if __name__ == "__main__":
    main()
