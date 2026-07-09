"""
Game - Main game loop and world management
"""

from typing import List, Dict, Optional
from .npc import NPC
from .llm_integration import GroqLLMClient
from .npc_interactions import NPCInteractionManager
from .world_events import WorldEventSystem, WorldEvent
from .visual_display import VisualDisplay


class Game:
    """
    Main game class that manages NPCs and the game world
    """
    
    def __init__(self, groq_api_key: Optional[str] = None):
        """Initialize the game"""
        self.npcs: Dict[str, NPC] = {}
        self.llm_client = None

        # Initialize LLM client if API key provided
        if groq_api_key:
            try:
                self.llm_client = GroqLLMClient(api_key=groq_api_key)
                print("✓ Groq LLM client initialized")
            except Exception as e:
                print(f"Warning: Could not initialize Groq client: {e}")

        self.current_npc: Optional[NPC] = None
        self.turn_count = 0

        # New systems
        self.interaction_manager = NPCInteractionManager()
        self.world_events = WorldEventSystem()
        self.visual_display = VisualDisplay()
    
    def add_npc(self, npc: NPC):
        """Add an NPC to the game"""
        npc.llm_client = self.llm_client
        self.npcs[npc.persona.name] = npc
        print(f"✓ Added NPC: {npc.persona.name}")
    
    def select_npc(self, name: str) -> bool:
        """Select an NPC to interact with"""
        if name in self.npcs:
            self.current_npc = self.npcs[name]
            return True
        return False
    
    def list_npcs(self) -> List[str]:
        """List all available NPCs"""
        return list(self.npcs.keys())
    
    def interact(self, player_input: str) -> str:
        """
        Player interacts with the current NPC
        
        Args:
            player_input: What the player says or does
            
        Returns:
            The NPC's response
        """
        if not self.current_npc:
            return "No NPC selected. Use 'talk to <name>' to select an NPC."
        
        self.turn_count += 1
        response = self.current_npc.interact(player_input)
        return response
    
    def get_current_npc_status(self) -> str:
        """Get status of the current NPC"""
        if not self.current_npc:
            return "No NPC selected"
        return self.current_npc.get_status()

    def trigger_npc_conversation(self, npc1_name: str, npc2_name: str, topic: str, turns: int = 3):
        """
        Make two NPCs talk to each other

        Args:
            npc1_name: First NPC name
            npc2_name: Second NPC name
            topic: What they discuss
            turns: Number of exchanges

        Returns:
            The conversation object
        """
        if npc1_name not in self.npcs or npc2_name not in self.npcs:
            print(f"Error: Both NPCs must exist")
            return None

        npc1 = self.npcs[npc1_name]
        npc2 = self.npcs[npc2_name]

        conversation = self.interaction_manager.npc_to_npc_exchange(npc1, npc2, topic, turns)

        # Spread any gossip generated
        for npc in self.npcs.values():
            self.interaction_manager.spread_gossip_to_npc(npc, count=1)

        return conversation

    def trigger_world_event(self, event_name: Optional[str] = None):
        """
        Trigger a world event (random if not specified)

        Args:
            event_name: Optional specific event name

        Returns:
            The triggered event
        """
        if event_name:
            # Custom event
            from .world_events import EventType
            event = self.world_events.create_custom_event(
                name=event_name,
                description=f"A significant event: {event_name}",
                event_type=EventType.POLITICAL,
                importance=7
            )
        else:
            # Random event
            event = self.world_events.trigger_random_event(min_importance=3)

        if event:
            # Notify all NPCs about the event
            for npc in self.npcs.values():
                npc.perception.observe_world_event(
                    event=f"{event.name}: {event.description}",
                    importance=event.importance,
                    turn=self.turn_count
                )

            return event
        return None

    def spread_gossip(self):
        """Spread gossip among all NPCs"""
        for npc in self.npcs.values():
            self.interaction_manager.spread_gossip_to_npc(npc, count=2)

    def get_gossip_network(self) -> List[str]:
        """Get all gossip in the network"""
        return self.interaction_manager.gossip_network
    
    def run_interactive_loop(self):
        """Run an interactive game loop in the terminal"""
        print("\n" + "="*60)
        print("   AI NPC GAME - NPCs with Soul")
        print("="*60)
        print("\nAvailable NPCs:")
        for i, name in enumerate(self.list_npcs(), 1):
            print(f"  {i}. {name}")
        
        print("\nCommands:")
        print("  'talk to <name>' - Select an NPC to talk to")
        print("  'status' - View current NPC's detailed card")
        print("  'history' - View conversation history with current NPC")
        print("  'list' - List all NPCs")
        print("  'overhear <npc1> <npc2>' - Listen to two NPCs talk")
        print("  'event' - Trigger a random world event")
        print("  'gossip' - See what gossip is spreading")
        print("  'world' - View world status")
        print("  'network' - View NPC relationship network")
        print("  'quit' - Exit the game")
        print("="*60)
        
        while True:
            print()
            if self.current_npc:
                user_input = input(f"[You -> {self.current_npc.persona.name}] ").strip()
            else:
                user_input = input("[You] ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == 'quit':
                print("\nThanks for playing!")
                break
            
            elif user_input.lower() == 'status':
                if self.current_npc:
                    print("\n" + self.visual_display.show_npc_card(self.current_npc, show_secrets=False))
                else:
                    print("No NPC selected")
                continue

            elif user_input.lower() == 'history':
                if self.current_npc:
                    print("\n" + self.visual_display.show_conversation_history(self.current_npc, count=10))
                else:
                    print("No NPC selected")
                continue
            
            elif user_input.lower() == 'list':
                print("\nAvailable NPCs:")
                for i, name in enumerate(self.list_npcs(), 1):
                    print(f"  {i}. {name}")
                continue
            
            elif user_input.lower().startswith('talk to '):
                npc_name = user_input[8:].strip()
                # Try to find NPC by partial name match
                matched_npc = None
                for name in self.npcs.keys():
                    if npc_name.lower() in name.lower():
                        matched_npc = name
                        break

                if matched_npc and self.select_npc(matched_npc):
                    print(f"\n[You approach {self.current_npc.persona.name}]")
                    print(f"[{self.current_npc.persona.name}]: Hello there.")
                else:
                    print(f"Could not find NPC: {npc_name}")
                continue

            elif user_input.lower().startswith('overhear '):
                # Parse "overhear npc1 npc2" - can be full names or partial
                remaining = user_input[9:].strip()

                # Try to find two NPC names in the input
                found_npcs = []
                for npc_name in self.npcs.keys():
                    if npc_name.lower() in remaining.lower():
                        found_npcs.append(npc_name)

                if len(found_npcs) < 2:
                    print("Could not find both NPCs in your input.")
                    print("Usage: overhear <npc1> <npc2>")
                    print("Example: overhear Greta Thorne")
                    print("Or: overhear Greta the Tavern Keeper Captain Thorne")
                    continue

                npc1_name = found_npcs[0]
                npc2_name = found_npcs[1]

                print(f"\n[You overhear {npc1_name} talking to {npc2_name}]")
                print("🤔 They're having a conversation...\n")

                # Random topic based on their personalities
                topics = [
                    "recent events in town",
                    "the player (you!)",
                    "their work and daily life",
                    "rumors they've heard"
                ]
                import random
                topic = random.choice(topics)

                conversation = self.trigger_npc_conversation(npc1_name, npc2_name, topic, turns=2)

                if conversation:
                    print(conversation.get_summary())
                continue

            elif user_input.lower() == 'event':
                event = self.trigger_world_event()
                if event:
                    print(f"\n{event.get_announcement()}")
                else:
                    print("\nNothing significant happens.")
                continue

            elif user_input.lower() == 'gossip':
                gossip_list = self.get_gossip_network()
                if gossip_list:
                    print("\n💬 Gossip Network:")
                    for i, gossip in enumerate(gossip_list[-5:], 1):
                        print(f"  {i}. {gossip}")
                else:
                    print("\nNo gossip circulating yet.")
                continue

            elif user_input.lower() == 'world':
                recent_events = self.world_events.get_recent_events(5)
                print("\n" + self.visual_display.show_world_status(recent_events, self.turn_count))
                continue

            elif user_input.lower() == 'network':
                print("\n" + self.visual_display.show_relationship_network(
                    self.npcs,
                    self.interaction_manager.npc_relationships
                ))
                continue
            
            # Regular interaction
            if not self.current_npc:
                print("You need to select an NPC first. Use 'talk to <name>'")
                continue
            
            # Get NPC response
            response = self.interact(user_input)
            print(f"\n[{self.current_npc.persona.name}]: {response}")


def create_demo_game(groq_api_key: Optional[str] = None) -> Game:
    """
    Create a demo game with pre-made NPCs
    
    Args:
        groq_api_key: Optional Groq API key
        
    Returns:
        Game instance with NPCs loaded
    """
    from .persona_core import create_tavern_keeper, create_mysterious_scholar, create_guard_captain
    
    game = Game(groq_api_key=groq_api_key)
    
    # Create NPCs
    greta = NPC(persona=create_tavern_keeper())
    aldric = NPC(persona=create_mysterious_scholar())
    thorne = NPC(persona=create_guard_captain())
    
    # Add them to the game
    game.add_npc(greta)
    game.add_npc(aldric)
    game.add_npc(thorne)
    
    return game
