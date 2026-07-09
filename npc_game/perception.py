"""
Perception Layer - What the NPC observes
Includes: player words + tone, world events, NPC gossip
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum


class Tone(Enum):
    """Player's tone of voice"""
    FRIENDLY = "friendly"
    NEUTRAL = "neutral"
    AGGRESSIVE = "aggressive"
    PLEADING = "pleading"
    DECEPTIVE = "deceptive"
    RESPECTFUL = "respectful"
    DISMISSIVE = "dismissive"


@dataclass
class Observation:
    """A single observation made by the NPC"""
    description: str
    tone: Optional[Tone] = None
    importance: int = 1  # 1-10, how important is this observation
    timestamp: int = 0  # Turn number when observed
    
    def to_text(self) -> str:
        """Convert observation to text for LLM"""
        text = self.description
        if self.tone:
            text += f" (tone: {self.tone.value})"
        return text


@dataclass
class PerceptionLayer:
    """
    Manages what the NPC perceives about the world and player
    """
    
    # Current observations
    current_observations: List[Observation] = field(default_factory=list)
    
    # World state knowledge
    world_state: Dict[str, str] = field(default_factory=dict)
    
    # Known gossip/rumors
    known_gossip: List[str] = field(default_factory=list)
    
    def observe_player_action(self, player_input: str, tone: Tone = Tone.NEUTRAL, turn: int = 0):
        """Record an observation of player words and actions"""
        obs = Observation(
            description=f"Player says: '{player_input}'",
            tone=tone,
            importance=5,
            timestamp=turn
        )
        self.current_observations.append(obs)
    
    def observe_world_event(self, event: str, importance: int = 3, turn: int = 0):
        """Record an observation of a world event"""
        obs = Observation(
            description=f"Event: {event}",
            importance=importance,
            timestamp=turn
        )
        self.current_observations.append(obs)
    
    def learn_gossip(self, gossip: str):
        """Learn a piece of gossip"""
        if gossip not in self.known_gossip:
            self.known_gossip.append(gossip)
    
    def update_world_state(self, key: str, value: str):
        """Update knowledge about the world state"""
        self.world_state[key] = value
    
    def get_recent_observations(self, count: int = 5) -> List[Observation]:
        """Get the most recent observations"""
        return sorted(
            self.current_observations,
            key=lambda x: x.timestamp,
            reverse=True
        )[:count]
    
    def get_important_observations(self, threshold: int = 5) -> List[Observation]:
        """Get observations above importance threshold"""
        return [obs for obs in self.current_observations if obs.importance >= threshold]
    
    def get_perception_context(self) -> str:
        """Generate perception context for LLM"""
        context = "## Current Observations:\n"
        
        # Recent observations
        recent = self.get_recent_observations(5)
        if recent:
            for obs in recent:
                context += f"- {obs.to_text()}\n"
        else:
            context += "- Nothing significant\n"
        
        # World state
        if self.world_state:
            context += "\n## Known World State:\n"
            for key, value in self.world_state.items():
                context += f"- {key}: {value}\n"
        
        # Gossip
        if self.known_gossip:
            context += "\n## Known Gossip:\n"
            for gossip in self.known_gossip[-3:]:  # Last 3 gossips
                context += f"- {gossip}\n"
        
        return context
    
    def clear_old_observations(self, keep_recent: int = 10):
        """Clear old observations to prevent overflow"""
        if len(self.current_observations) > keep_recent:
            # Keep the most recent and most important
            recent = sorted(self.current_observations, key=lambda x: x.timestamp, reverse=True)[:keep_recent//2]
            important = sorted(self.current_observations, key=lambda x: x.importance, reverse=True)[:keep_recent//2]

            # Combine and deduplicate by creating a dict with unique ids
            seen = {}
            for obs in recent + important:
                obs_id = id(obs)
                if obs_id not in seen:
                    seen[obs_id] = obs

            self.current_observations = list(seen.values())


def analyze_player_tone(player_input: str) -> Tone:
    """
    Simple heuristic to analyze player's tone from their input.
    In a real system, you might use the LLM for this.
    """
    player_lower = player_input.lower()
    
    # Aggressive indicators
    if any(word in player_lower for word in ['attack', 'threaten', 'kill', 'fight', 'die', '!']):
        if player_lower.count('!') >= 2:
            return Tone.AGGRESSIVE
    
    # Pleading indicators
    if any(word in player_lower for word in ['please', 'beg', 'help me', 'need']):
        return Tone.PLEADING
    
    # Friendly indicators
    if any(word in player_lower for word in ['friend', 'thank', 'appreciate', 'wonderful', 'great']):
        return Tone.FRIENDLY
    
    # Respectful indicators
    if any(word in player_lower for word in ['sir', 'madam', 'lord', 'lady', 'honored']):
        return Tone.RESPECTFUL
    
    # Dismissive indicators
    if any(word in player_lower for word in ['whatever', 'don\'t care', 'boring', 'waste']):
        return Tone.DISMISSIVE
    
    return Tone.NEUTRAL
