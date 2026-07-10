"""
Living World Demo
Watch the world come alive with autonomous NPCs
"""

from npc_game.enhanced_npc import EnhancedNPC
from npc_game.persona_core import PersonaCore
from npc_game.living_world import LivingWorld
from npc_game.llm_integration import GroqLLMClient
from npc_game.config import GROQ_API_KEY
import time


def create_sample_npcs():
    """Create some sample NPCs for the world"""
    
    # The Tavern Keeper
    greta = EnhancedNPC(
        persona=PersonaCore(
            name="Greta",
            occupation="Tavern Keeper (45 years old)",
            traits=["friendly", "observant", "gossipy", "protective"],
            backstory="Runs the Rusty Flagon tavern for 20 years. Knows everyone's secrets.",
            core_motive="Keep the tavern profitable and customers happy",
            beliefs=["Good ale solves most problems", "Everyone deserves a hot meal"],
            secrets=["Waters down the cheap ale", "Has a crush on the blacksmith"]
        ),
        current_location="tavern",
        home_location="tavern",
        work_location="tavern"
    )

    # The Guard Captain
    marcus = EnhancedNPC(
        persona=PersonaCore(
            name="Captain Marcus",
            occupation="Town Guard Captain (38 years old)",
            traits=["honorable", "stern", "vigilant", "distrustful"],
            backstory="Rose through ranks. Obsessed with catching the mysterious thief.",
            core_motive="Maintain law and order, catch criminals",
            beliefs=["Justice must be served", "Trust must be earned"],
            secrets=["Secretly takes bribes from merchants", "Failed to save his brother years ago"]
        ),
        current_location="guard_house",
        home_location="guard_house",
        work_location="guard_house"
    )

    # The Mysterious Scholar
    elara = EnhancedNPC(
        persona=PersonaCore(
            name="Elara",
            occupation="Scholar (29 years old)",
            traits=["intelligent", "curious", "secretive", "eccentric"],
            backstory="Traveled from the capital to research ancient ruins nearby.",
            core_motive="Uncover the secrets of the old ruins",
            beliefs=["Knowledge is power", "Magic still exists in the world"],
            secrets=["Actually a spy for the capital", "Found a magical artifact in the ruins"]
        ),
        current_location="market",
        home_location="merchant_quarter",
        work_location="merchant_quarter"
    )
    
    return [greta, marcus, elara]


def main():
    """Run the living world demo"""
    
    print("🌍 LIVING WORLD SIMULATION")
    print("=" * 70)
    print()
    
    # Initialize LLM client (optional)
    llm_client = None
    try:
        if GROQ_API_KEY:
            llm_client = GroqLLMClient(api_key=GROQ_API_KEY)
            print("✓ LLM client initialized")
    except Exception as e:
        print(f"⚠️  LLM client not available: {e}")
        print("   NPCs will use simpler responses")
    
    print()
    
    # Create the living world
    world = LivingWorld(llm_client=llm_client)
    
    # Add NPCs
    npcs = create_sample_npcs()
    for npc in npcs:
        world.add_npc(npc)
    
    print()
    print("=" * 70)
    print("INITIAL WORLD STATE")
    print("=" * 70)
    print(world.get_world_summary())
    
    print("\n" + "=" * 70)
    print("STARTING SIMULATION...")
    print("=" * 70)
    
    # Run simulation
    print("\n⏩ Simulating 12 ticks (3 game hours)...\n")
    
    try:
        world.run_simulation(ticks=12, verbose=True)
    except KeyboardInterrupt:
        print("\n\n⏸️  Simulation paused by user")
    
    # Show final state
    print("\n" + "=" * 70)
    print("FINAL WORLD STATE")
    print("=" * 70)
    print(world.get_world_summary())
    
    # Show gossip
    print("\n" + "=" * 70)
    print("GOSSIP NETWORK")
    print("=" * 70)
    for npc_name in world.npcs.keys():
        print(world.gossip.get_summary(npc_name))
        print()
    
    # Interactive mode
    print("\n" + "=" * 70)
    print("INTERACTIVE MODE")
    print("=" * 70)
    print("You can now interact with NPCs or continue simulation")
    print("Commands:")
    print("  talk <npc_name> <message> - Talk to an NPC")
    print("  tick <n>                  - Run n simulation ticks")
    print("  status                    - Show world status")
    print("  quit                      - Exit")
    print()
    
    while True:
        try:
            cmd = input(">>> ").strip()
            
            if not cmd:
                continue
            
            if cmd.lower() == "quit":
                break
            
            elif cmd.lower() == "status":
                print(world.get_world_summary())
            
            elif cmd.lower().startswith("tick"):
                parts = cmd.split()
                n = int(parts[1]) if len(parts) > 1 else 1
                world.run_simulation(ticks=n, verbose=True)
            
            elif cmd.lower().startswith("talk"):
                parts = cmd.split(maxsplit=2)
                if len(parts) >= 3:
                    npc_name = parts[1].capitalize()
                    message = parts[2]
                    response = world.player_interact_with_npc(npc_name, message)
                    print(f"\n{npc_name}: {response}\n")
                else:
                    print("Usage: talk <npc_name> <message>")
            
            else:
                print("Unknown command. Try: talk, tick, status, or quit")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n👋 Simulation ended. Goodbye!")


if __name__ == "__main__":
    main()
