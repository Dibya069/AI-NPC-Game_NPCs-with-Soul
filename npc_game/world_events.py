"""
World Events System
Dynamic events that affect NPCs and the game world
"""

from typing import List, Dict, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum
import random


class EventType(Enum):
    """Types of world events"""
    WEATHER = "weather"
    CRIME = "crime"
    CELEBRATION = "celebration"
    DISASTER = "disaster"
    POLITICAL = "political"
    ECONOMIC = "economic"
    SUPERNATURAL = "supernatural"


@dataclass
class WorldEvent:
    """A single world event"""
    name: str
    description: str
    event_type: EventType
    importance: int  # 1-10, how significant is this event
    turn_occurred: int
    affects_all: bool = True  # Does this affect all NPCs?
    
    def get_announcement(self) -> str:
        """Get an announcement text for this event"""
        return f"🌍 [WORLD EVENT] {self.name}: {self.description}"


class WorldEventSystem:
    """
    Manages dynamic world events that NPCs can react to
    """
    
    def __init__(self):
        self.events_history: List[WorldEvent] = []
        self.active_events: List[WorldEvent] = []
        self.current_turn: int = 0
        self.event_templates = self._create_event_templates()
    
    def _create_event_templates(self) -> List[Dict]:
        """Create templates for random events"""
        return [
            # Weather events
            {
                "name": "Sudden Storm",
                "description": "Dark clouds gather and rain pours down",
                "type": EventType.WEATHER,
                "importance": 3
            },
            {
                "name": "Beautiful Sunrise",
                "description": "A gorgeous sunrise paints the sky golden",
                "type": EventType.WEATHER,
                "importance": 2
            },
            # Crime events
            {
                "name": "Theft at the Market",
                "description": "Someone stole goods from the market stalls",
                "type": EventType.CRIME,
                "importance": 6
            },
            {
                "name": "Mysterious Murder",
                "description": "A body was found in the alley behind the tavern",
                "type": EventType.CRIME,
                "importance": 9
            },
            {
                "name": "Pickpocket Caught",
                "description": "The guards caught a thief in the act",
                "type": EventType.CRIME,
                "importance": 4
            },
            # Celebration events
            {
                "name": "Festival Day",
                "description": "The town is celebrating with music and dancing",
                "type": EventType.CELEBRATION,
                "importance": 7
            },
            {
                "name": "Royal Visitor",
                "description": "A noble from the capital has arrived in town",
                "type": EventType.POLITICAL,
                "importance": 8
            },
            # Economic events
            {
                "name": "Merchant Caravan Arrives",
                "description": "A large merchant caravan brought exotic goods",
                "type": EventType.ECONOMIC,
                "importance": 5
            },
            {
                "name": "Crop Shortage",
                "description": "Poor harvest means food prices are rising",
                "type": EventType.ECONOMIC,
                "importance": 7
            },
            # Supernatural events
            {
                "name": "Strange Lights",
                "description": "Eerie lights were seen in the forest last night",
                "type": EventType.SUPERNATURAL,
                "importance": 6
            },
            {
                "name": "Ghostly Apparition",
                "description": "Several people claim to have seen a ghost",
                "type": EventType.SUPERNATURAL,
                "importance": 7
            },
            # Disaster events
            {
                "name": "Building Fire",
                "description": "A fire broke out in the workshop district",
                "type": EventType.DISASTER,
                "importance": 8
            },
        ]
    
    def trigger_event(self, event: WorldEvent) -> WorldEvent:
        """Trigger a specific world event"""
        event.turn_occurred = self.current_turn
        self.events_history.append(event)
        self.active_events.append(event)
        return event
    
    def trigger_random_event(self, min_importance: int = 3) -> Optional[WorldEvent]:
        """Trigger a random event from templates"""
        # Filter by minimum importance
        valid_templates = [t for t in self.event_templates if t["importance"] >= min_importance]
        
        if not valid_templates:
            return None
        
        template = random.choice(valid_templates)
        
        event = WorldEvent(
            name=template["name"],
            description=template["description"],
            event_type=template["type"],
            importance=template["importance"],
            turn_occurred=self.current_turn
        )
        
        return self.trigger_event(event)
    
    def get_recent_events(self, count: int = 3) -> List[WorldEvent]:
        """Get the most recent events"""
        return sorted(self.events_history, key=lambda e: e.turn_occurred, reverse=True)[:count]
    
    def get_active_events(self) -> List[WorldEvent]:
        """Get currently active events"""
        return self.active_events
    
    def get_event_summary(self) -> str:
        """Get a summary of recent events for context"""
        recent = self.get_recent_events(3)
        if not recent:
            return "No significant world events recently."
        
        summary = "Recent World Events:\n"
        for event in recent:
            summary += f"- {event.name}: {event.description}\n"
        
        return summary
    
    def clear_old_events(self, max_active: int = 5):
        """Clear old active events"""
        if len(self.active_events) > max_active:
            self.active_events = sorted(
                self.active_events,
                key=lambda e: e.turn_occurred,
                reverse=True
            )[:max_active]
    
    def advance_turn(self):
        """Advance the turn counter"""
        self.current_turn += 1
    
    def create_custom_event(self, name: str, description: str, 
                           event_type: EventType, importance: int = 5) -> WorldEvent:
        """Create and trigger a custom event"""
        event = WorldEvent(
            name=name,
            description=description,
            event_type=event_type,
            importance=importance,
            turn_occurred=self.current_turn
        )
        return self.trigger_event(event)


def get_npc_reaction_to_event(npc_traits: List[str], event: WorldEvent) -> str:
    """
    Generate a simple reaction template based on NPC traits and event type
    This can be used as additional context for the LLM
    """
    reactions = []
    
    # Trait-based reactions
    if "brave" in npc_traits and event.event_type in [EventType.CRIME, EventType.DISASTER]:
        reactions.append("feels compelled to help")
    
    if "greedy" in npc_traits and event.event_type == EventType.ECONOMIC:
        reactions.append("sees this as an opportunity for profit")
    
    if "paranoid" in npc_traits and event.event_type == EventType.SUPERNATURAL:
        reactions.append("is deeply concerned and suspicious")
    
    if "jovial" in npc_traits and event.event_type == EventType.CELEBRATION:
        reactions.append("is excited and wants to join in")
    
    # Event-based reactions
    if event.importance >= 8:
        reactions.append("considers this very significant")
    
    if not reactions:
        reactions.append("is aware of this event")
    
    return f"This NPC likely {' and '.join(reactions)}."
