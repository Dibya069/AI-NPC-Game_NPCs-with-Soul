"""
Example usage of the AI NPC system
Shows how to create custom NPCs and use the system programmatically
"""

import os
from npc_game.persona_core import PersonaCore
from npc_game.npc import NPC
from npc_game.game import Game
from npc_game.llm_integration import GroqLLMClient


def example_1_simple_conversation():
    """Example 1: Simple conversation with a pre-made NPC"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple Conversation")
    print("="*60)
    
    from npc_game.persona_core import create_tavern_keeper
    
    # Create NPC
    greta = NPC(persona=create_tavern_keeper())
    
    # Set up LLM (if API key available)
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        greta.llm_client = GroqLLMClient(api_key=api_key)
    
    # Have a conversation
    print("\n[You approach Greta the Tavern Keeper]")
    
    response = greta.interact("Hello! What's the best drink you have?")
    print(f"[Greta]: {response}")
    
    response = greta.interact("I'm looking for information about the mayor. What do you know?")
    print(f"[Greta]: {response}")
    
    # Check status
    print(greta.get_status())


def example_2_custom_npc():
    """Example 2: Create a custom NPC from scratch"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Custom NPC Creation")
    print("="*60)
    
    # Create a custom persona
    blacksmith_persona = PersonaCore(
        name="Thorin Ironforge",
        occupation="Master Blacksmith",
        traits=["gruff", "perfectionist", "secretly kind-hearted", "proud"],
        backstory="Thorin has been smithing for 40 years. He lost his son in a mining accident and blames himself for making faulty equipment.",
        core_motive="Wants to create the perfect sword to honor his son's memory",
        beliefs=[
            "Quality over quantity, always",
            "A craftsman's work is their legacy",
            "Never compromise on safety"
        ],
        secrets=[
            "He still cries when working with the ore from the mine where his son died",
            "He's been secretly helping poor families for free"
        ],
        relationships={
            "Guild Master": "Respects but disagrees on production quotas",
            "His son": "Deceased, deep guilt and love"
        }
    )
    
    # Create NPC
    thorin = NPC(persona=blacksmith_persona)
    
    # Set up LLM
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        thorin.llm_client = GroqLLMClient(api_key=api_key)
    
    # Interact
    print("\n[You enter the forge]")
    
    response = thorin.interact("Master Thorin, I need a sword!")
    print(f"[Thorin]: {response}")
    
    response = thorin.interact("I'm willing to pay well. This is urgent!")
    print(f"[Thorin]: {response}")
    
    print(thorin.get_status())


def example_3_game_with_multiple_npcs():
    """Example 3: Full game with multiple NPCs"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Multi-NPC Game")
    print("="*60)
    
    # Create game
    api_key = os.getenv('GROQ_API_KEY')
    game = Game(groq_api_key=api_key)
    
    # Add multiple NPCs
    from npc_game.persona_core import create_tavern_keeper, create_mysterious_scholar
    
    game.add_npc(NPC(persona=create_tavern_keeper()))
    game.add_npc(NPC(persona=create_mysterious_scholar()))
    
    # Interact with different NPCs
    game.select_npc("Greta the Tavern Keeper")
    print("\n[Talking to Greta]")
    response = game.interact("Have you seen any strange scholars around?")
    print(f"[Greta]: {response}")
    
    game.select_npc("Aldric the Scholar")
    print("\n[Talking to Aldric]")
    response = game.interact("What are you researching?")
    print(f"[Aldric]: {response}")
    
    # Show status
    print(game.get_current_npc_status())


def example_4_emotion_and_memory():
    """Example 4: Demonstrate emotion changes and memory"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Emotions and Memory")
    print("="*60)
    
    from npc_game.persona_core import create_guard_captain
    
    # Create NPC
    thorne = NPC(persona=create_guard_captain())
    
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        thorne.llm_client = GroqLLMClient(api_key=api_key)
    
    print("\n[Meeting Captain Thorne]")
    
    # Friendly interaction
    response = thorne.interact("Good morning, Captain! Beautiful day, isn't it?")
    print(f"[Thorne]: {response}")
    print(f"Status: {thorne.decision_engine.emotion_state.to_text()}")
    
    # Aggressive interaction
    response = thorne.interact("You guards are useless! There are thieves everywhere!")
    print(f"\n[Thorne]: {response}")
    print(f"Status: {thorne.decision_engine.emotion_state.to_text()}")
    
    # Check if he remembers
    response = thorne.interact("Sorry about that. I was just frustrated.")
    print(f"\n[Thorne]: {response}")
    print(f"Status: {thorne.decision_engine.emotion_state.to_text()}")
    
    # Show memory
    print("\n" + thorne.decision_engine.memory.get_memory_context())


if __name__ == "__main__":
    print("AI NPC System - Examples\n")
    print("Make sure GROQ_API_KEY is set in your environment!")
    print("Get a free key at: https://console.groq.com/\n")
    
    # Run examples
    try:
        example_1_simple_conversation()
        example_2_custom_npc()
        example_3_game_with_multiple_npcs()
        example_4_emotion_and_memory()
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Make sure you have set GROQ_API_KEY environment variable!")
