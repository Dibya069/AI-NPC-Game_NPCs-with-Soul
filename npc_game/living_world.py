"""
Living World Game Manager
Orchestrates the entire living world simulation
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
import random

from .enhanced_npc import EnhancedNPC
from .world_simulation import WorldSimulation
from .gossip_system import GossipSystem, Information, InformationType
from .economy import Economy
from .world_events import WorldEventSystem, WorldEvent, EventType
from .llm_integration import GroqLLMClient


@dataclass
class LivingWorld:
    """
    The complete living world system
    Manages NPCs, world state, economy, and autonomous behavior
    """
    
    # All systems
    world: WorldSimulation = field(default_factory=WorldSimulation)
    gossip: GossipSystem = field(default_factory=GossipSystem)
    economy: Economy = field(default_factory=Economy)
    events: WorldEventSystem = field(default_factory=WorldEventSystem)
    
    # NPCs
    npcs: Dict[str, EnhancedNPC] = field(default_factory=dict)
    
    # LLM client
    llm_client: Optional[GroqLLMClient] = None
    
    # Simulation settings
    auto_simulate: bool = False
    ticks_per_action: int = 4  # How many ticks between NPC actions
    
    def __post_init__(self):
        """Initialize the living world"""
        pass
    
    def add_npc(self, npc: EnhancedNPC):
        """Add an NPC to the world"""
        npc.llm_client = self.llm_client
        self.npcs[npc.persona.name] = npc
        
        # Register NPC at their current location
        self.world.npc_at_location(npc.persona.name, npc.current_location)
        
        print(f"✓ Added {npc.persona.name} to the world at {npc.current_location}")
    
    def simulate_tick(self) -> Dict[str, List[str]]:
        """
        Run one simulation tick
        Returns dictionary of events by category
        """
        tick_events = {
            "world": [],
            "npcs": [],
            "economy": [],
            "gossip": [],
            "events": []
        }
        
        # 1. World time and weather update
        world_status = self.world.tick()
        tick_events["world"].append(f"⏰ {world_status['time']}")
        tick_events["world"].append(f"{world_status['weather']}")
        
        # 2. NPCs act autonomously
        for npc_name, npc in self.npcs.items():
            # Update NPC location in world
            old_location = self.world.get_npcs_at_location(npc.current_location)
            
            # NPC takes autonomous action
            action_result = npc.autonomous_tick()
            tick_events["npcs"].append(f"{npc.persona.name}: {action_result}")
            
            # Update location if changed
            if npc.current_location not in old_location:
                self.world.npc_at_location(npc.persona.name, npc.current_location)
        
        # 3. NPC-to-NPC interactions at same location
        for location_name, location in self.world.locations.items():
            npcs_here = location.get_present_npcs()
            
            if len(npcs_here) >= 2:
                # NPCs at same location might share gossip
                npc1_name = npcs_here[0]
                npc2_name = npcs_here[1]
                
                shared_info = self.gossip.npcs_share_information(npc1_name, npc2_name, 0.5)
                
                if shared_info:
                    tick_events["gossip"].append(
                        f"💬 {npc1_name} and {npc2_name} exchange gossip at {location_name}"
                    )
        
        # 4. Random world events (low probability)
        if random.random() < 0.1:  # 10% chance each tick
            event = self.events.trigger_random_event(min_importance=4)
            if event:
                tick_events["events"].append(f"🌍 {event.get_announcement()}")
                
                # Apply economic effects
                self.economy.apply_event_effect(event.description)
                
                # Create gossip about the event
                self.gossip.create_news(
                    content=event.description,
                    source="world",
                    importance=event.importance
                )
        
        # 5. Market fluctuations (every few ticks)
        if self.world.tick_count % 10 == 0:
            self.economy.update_market()
            tick_events["economy"].append("💰 Market prices fluctuate")
        
        # 6. Advance turn counters
        self.gossip.advance_turn()
        self.events.advance_turn()
        
        return tick_events
    
    def get_world_summary(self) -> str:
        """Get comprehensive world summary"""
        lines = [
            self.world.get_world_status(),
            "",
            "👥 NPC STATUS:",
            "=" * 50
        ]
        
        for npc_name, npc in self.npcs.items():
            lines.append(f"\n📍 {npc.persona.name} @ {npc.current_location}")
            lines.append(f"   {npc.inventory.get_summary()}")
            
            # Show current plan
            current_plan = npc.planner.get_current_plan()
            if current_plan:
                lines.append(f"   📋 Plan: {current_plan.goal} [{current_plan.get_progress()}]")
            
            # Show most urgent need
            urgent_need = npc.needs.get_most_urgent_need()
            if urgent_need:
                need_value = npc.needs.needs[urgent_need].value
                lines.append(f"   ⚠️  Urgent: {urgent_need.value} ({int(need_value)}%)")
        
        lines.append("\n" + "=" * 50)
        lines.append(self.economy.get_price_list())
        
        return "\n".join(lines)
    
    def run_simulation(self, ticks: int = 1, verbose: bool = True) -> List[Dict]:
        """
        Run simulation for N ticks
        Returns list of tick events
        """
        all_events = []
        
        for i in range(ticks):
            tick_events = self.simulate_tick()
            all_events.append(tick_events)
            
            if verbose:
                print(f"\n{'='*60}")
                print(f"TICK {self.world.tick_count}")
                print('='*60)
                
                for category, events in tick_events.items():
                    if events:
                        print(f"\n[{category.upper()}]")
                        for event in events:
                            print(f"  {event}")
        
        return all_events
    
    def player_interact_with_npc(self, npc_name: str, player_input: str) -> str:
        """Player interacts with an NPC"""
        if npc_name not in self.npcs:
            return f"❌ {npc_name} not found in the world"
        
        npc = self.npcs[npc_name]
        response = npc.interact(player_input)
        
        # Create gossip about player interaction
        self.gossip.add_information(Information(
            content=f"The player spoke with {npc_name}",
            info_type=InformationType.RUMOR,
            source=npc_name,
            importance=3
        ))
        
        return response
