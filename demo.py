#!/usr/bin/env python
"""
Quick Demo - Test the AI NPC system
"""

import os
import sys


def check_api_key():
    """Check if GROQ_API_KEY is set"""
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ GROQ_API_KEY not found!")
        print("\n📝 To get started:")
        print("   1. Visit: https://console.groq.com/")
        print("   2. Sign up and get a FREE API key")
        print("   3. Set it: export GROQ_API_KEY='your-key-here'")
        print("   4. Run this script again")
        return False
    
    print("✅ GROQ_API_KEY found!")
    return True


def test_imports():
    """Test that all imports work"""
    print("\n🔍 Checking dependencies...")
    
    try:
        from groq import Groq
        print("✅ groq library installed")
    except ImportError:
        print("❌ groq library not found")
        print("   Install it: pip install groq")
        return False
    
    try:
        from npc_game.persona_core import create_tavern_keeper
        from npc_game.npc import NPC
        from npc_game.llm_integration import GroqLLMClient
        print("✅ npc_game package loaded")
    except ImportError as e:
        print(f"❌ Error loading npc_game: {e}")
        return False
    
    return True


def run_quick_test():
    """Run a quick conversation test"""
    print("\n🎮 Running quick NPC conversation test...\n")
    print("="*60)
    
    from npc_game.persona_core import create_tavern_keeper
    from npc_game.npc import NPC
    from npc_game.llm_integration import GroqLLMClient
    
    # Create NPC
    greta = NPC(persona=create_tavern_keeper())
    greta.llm_client = GroqLLMClient(api_key=os.getenv('GROQ_API_KEY'))
    
    print("✨ Created: Greta the Tavern Keeper")
    print("="*60)
    
    # Test conversation
    test_messages = [
        "Hello! What's your name?",
        "What's the best drink you have here?",
        "Have you heard any interesting rumors lately?"
    ]
    
    for i, msg in enumerate(test_messages, 1):
        print(f"\n[Turn {i}] You: {msg}")
        print("🤔 Thinking...")
        
        response = greta.interact(msg)
        print(f"[Greta]: {response}")
        print(f"\n📊 Status: {greta.decision_engine.emotion_state.to_text()} | Trust: {greta.player_trust}/100")
    
    print("\n" + "="*60)
    print("✅ Test completed successfully!")
    print("\n💡 The NPC system is working! Try:")
    print("   - python main.py (interactive game)")
    print("   - python example_usage.py (detailed examples)")


def main():
    print("🎭 AI NPC System - Quick Demo")
    print("="*60)
    
    # Check setup
    if not check_api_key():
        sys.exit(1)
    
    if not test_imports():
        sys.exit(1)
    
    # Run test
    try:
        run_quick_test()
    except KeyboardInterrupt:
        print("\n\n⏸️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
