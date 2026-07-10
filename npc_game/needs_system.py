"""
NPC Needs System
NPCs have dynamic needs that drive their behavior
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
from enum import Enum


class NeedType(Enum):
    """Types of NPC needs"""
    HUNGER = "hunger"
    ENERGY = "energy"
    SOCIAL = "social"
    SAFETY = "safety"
    WEALTH = "wealth"
    CURIOSITY = "curiosity"


@dataclass
class Need:
    """A single need with current value"""
    need_type: NeedType
    value: float = 50.0  # 0 (desperate) to 100 (satisfied)
    decay_rate: float = 1.0  # How fast it decreases per tick
    
    def update(self):
        """Decrease need over time"""
        self.value = max(0, self.value - self.decay_rate)
    
    def satisfy(self, amount: float):
        """Increase need satisfaction"""
        self.value = min(100, self.value + amount)
    
    def is_critical(self) -> bool:
        """Check if need is critically low"""
        return self.value < 20
    
    def is_urgent(self) -> bool:
        """Check if need is urgent"""
        return self.value < 40
    
    def get_priority(self) -> int:
        """Get priority level (higher = more urgent)"""
        if self.value < 20:
            return 10  # Critical
        elif self.value < 40:
            return 7   # Urgent
        elif self.value < 60:
            return 4   # Moderate
        else:
            return 1   # Low priority


@dataclass
class NeedsSystem:
    """Manages all needs for an NPC"""
    
    needs: Dict[NeedType, Need] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize all needs"""
        if not self.needs:
            self.needs = {
                NeedType.HUNGER: Need(NeedType.HUNGER, value=70, decay_rate=2.0),
                NeedType.ENERGY: Need(NeedType.ENERGY, value=80, decay_rate=1.5),
                NeedType.SOCIAL: Need(NeedType.SOCIAL, value=60, decay_rate=0.5),
                NeedType.SAFETY: Need(NeedType.SAFETY, value=90, decay_rate=0.1),
                NeedType.WEALTH: Need(NeedType.WEALTH, value=50, decay_rate=0.3),
                NeedType.CURIOSITY: Need(NeedType.CURIOSITY, value=40, decay_rate=0.8),
            }
    
    def update_all(self):
        """Update all needs (called each tick)"""
        for need in self.needs.values():
            need.update()
    
    def satisfy_need(self, need_type: NeedType, amount: float):
        """Satisfy a specific need"""
        if need_type in self.needs:
            self.needs[need_type].satisfy(amount)
    
    def get_most_urgent_need(self) -> Optional[NeedType]:
        """Get the most urgent need"""
        urgent_needs = [(need_type, need.get_priority()) 
                       for need_type, need in self.needs.items()]
        
        if not urgent_needs:
            return None
        
        # Sort by priority (highest first)
        urgent_needs.sort(key=lambda x: x[1], reverse=True)
        
        # Only return if it's at least moderately urgent
        if urgent_needs[0][1] >= 4:
            return urgent_needs[0][0]
        
        return None
    
    def get_critical_needs(self) -> list[NeedType]:
        """Get all critical needs"""
        return [need_type for need_type, need in self.needs.items() 
                if need.is_critical()]
    
    def get_status_summary(self) -> str:
        """Get a summary of current needs"""
        lines = ["Needs Status:"]
        for need_type, need in self.needs.items():
            emoji = self._get_need_emoji(need_type)
            bar = self._get_need_bar(need.value)
            status = "CRITICAL" if need.is_critical() else "Urgent" if need.is_urgent() else "OK"
            lines.append(f"  {emoji} {need_type.value.capitalize()}: {bar} {int(need.value)}% [{status}]")
        return "\n".join(lines)
    
    def _get_need_emoji(self, need_type: NeedType) -> str:
        """Get emoji for need type"""
        emojis = {
            NeedType.HUNGER: "🍖",
            NeedType.ENERGY: "⚡",
            NeedType.SOCIAL: "👥",
            NeedType.SAFETY: "🛡️",
            NeedType.WEALTH: "💰",
            NeedType.CURIOSITY: "🔍"
        }
        return emojis.get(need_type, "❓")
    
    def _get_need_bar(self, value: float) -> str:
        """Get visual bar for need value"""
        filled = int(value / 10)
        empty = 10 - filled
        return "█" * filled + "░" * empty
    
    def get_behavior_modifier(self) -> Dict[str, float]:
        """Get behavior modifiers based on needs"""
        modifiers = {
            "aggression": 0.0,
            "friendliness": 0.0,
            "risk_taking": 0.0,
            "talkativeness": 0.0
        }
        
        # Critical hunger makes NPCs desperate
        if self.needs[NeedType.HUNGER].is_critical():
            modifiers["aggression"] += 0.3
            modifiers["risk_taking"] += 0.4
        
        # Low energy makes NPCs irritable and less social
        if self.needs[NeedType.ENERGY].is_critical():
            modifiers["friendliness"] -= 0.3
            modifiers["talkativeness"] -= 0.4
        
        # Low social makes NPCs want interaction
        if self.needs[NeedType.SOCIAL].is_urgent():
            modifiers["talkativeness"] += 0.3
            modifiers["friendliness"] += 0.2
        
        # Low safety makes NPCs paranoid
        if self.needs[NeedType.SAFETY].is_urgent():
            modifiers["aggression"] += 0.2
            modifiers["risk_taking"] -= 0.5
        
        return modifiers
