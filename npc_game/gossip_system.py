"""
Gossip and Information Spreading System
Information spreads organically between NPCs
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional
from enum import Enum
import random


class InformationType(Enum):
    """Types of information that can spread"""
    RUMOR = "rumor"
    FACT = "fact"
    OPINION = "opinion"
    SECRET = "secret"
    WARNING = "warning"
    NEWS = "news"


@dataclass
class Information:
    """A piece of information that can spread"""
    content: str
    info_type: InformationType
    source: str  # Who started this information
    reliability: float = 0.8  # 0-1, how reliable is this
    importance: int = 5  # 1-10
    spread_count: int = 0  # How many NPCs know this
    turn_created: int = 0
    
    def degrade_reliability(self):
        """Information becomes less reliable as it spreads (like telephone game)"""
        self.reliability *= 0.95  # 5% degradation each spread
    
    def is_stale(self, current_turn: int, max_age: int = 50) -> bool:
        """Check if information is too old"""
        return (current_turn - self.turn_created) > max_age


@dataclass
class GossipSystem:
    """Manages information spreading between NPCs"""
    
    # Global information pool
    information_pool: List[Information] = field(default_factory=list)
    
    # What each NPC knows (NPC name -> list of information IDs)
    npc_knowledge: Dict[str, Set[int]] = field(default_factory=dict)
    
    current_turn: int = 0
    
    def add_information(self, info: Information) -> int:
        """Add new information to the pool"""
        info.turn_created = self.current_turn
        self.information_pool.append(info)
        info_id = len(self.information_pool) - 1
        
        # Source NPC knows this information
        if info.source not in self.npc_knowledge:
            self.npc_knowledge[info.source] = set()
        self.npc_knowledge[info.source].add(info_id)
        
        return info_id
    
    def npc_learns_info(self, npc_name: str, info_id: int):
        """NPC learns a piece of information"""
        if npc_name not in self.npc_knowledge:
            self.npc_knowledge[npc_name] = set()
        
        if info_id not in self.npc_knowledge[npc_name]:
            self.npc_knowledge[npc_name].add(info_id)
            
            # Update spread count
            if info_id < len(self.information_pool):
                self.information_pool[info_id].spread_count += 1
                self.information_pool[info_id].degrade_reliability()
    
    def npcs_share_information(self, npc1: str, npc2: str, 
                               share_chance: float = 0.7) -> List[Information]:
        """Two NPCs share information when they meet"""
        shared = []
        
        # Get what each knows
        knowledge1 = self.npc_knowledge.get(npc1, set())
        knowledge2 = self.npc_knowledge.get(npc2, set())
        
        # NPC1 shares with NPC2
        for info_id in knowledge1:
            if info_id not in knowledge2 and random.random() < share_chance:
                info = self.information_pool[info_id]
                
                # Don't share secrets easily
                if info.info_type == InformationType.SECRET:
                    if random.random() > 0.3:  # Only 30% chance
                        continue
                
                self.npc_learns_info(npc2, info_id)
                shared.append(info)
        
        # NPC2 shares with NPC1
        for info_id in knowledge2:
            if info_id not in knowledge1 and random.random() < share_chance:
                info = self.information_pool[info_id]
                
                if info.info_type == InformationType.SECRET:
                    if random.random() > 0.3:
                        continue
                
                self.npc_learns_info(npc1, info_id)
                shared.append(info)
        
        return shared
    
    def get_npc_knowledge(self, npc_name: str) -> List[Information]:
        """Get all information known by an NPC"""
        knowledge_ids = self.npc_knowledge.get(npc_name, set())
        return [self.information_pool[i] for i in knowledge_ids 
                if i < len(self.information_pool)]
    
    def get_recent_information(self, npc_name: str, count: int = 3) -> List[Information]:
        """Get most recent information known by NPC"""
        knowledge = self.get_npc_knowledge(npc_name)
        # Sort by turn created (most recent first)
        knowledge.sort(key=lambda x: x.turn_created, reverse=True)
        return knowledge[:count]
    
    def get_important_information(self, npc_name: str, min_importance: int = 7) -> List[Information]:
        """Get important information known by NPC"""
        knowledge = self.get_npc_knowledge(npc_name)
        return [info for info in knowledge if info.importance >= min_importance]
    
    def cleanup_stale_information(self):
        """Remove old, unimportant information"""
        # Remove stale info from pool
        self.information_pool = [
            info for info in self.information_pool
            if not info.is_stale(self.current_turn) or info.importance >= 8
        ]
        
        # Update NPC knowledge to remove deleted info
        valid_ids = set(range(len(self.information_pool)))
        for npc_name in self.npc_knowledge:
            self.npc_knowledge[npc_name] &= valid_ids
    
    def advance_turn(self):
        """Advance the turn counter"""
        self.current_turn += 1
    
    def create_rumor(self, content: str, source: str, importance: int = 5) -> Information:
        """Helper to create and add a rumor"""
        info = Information(
            content=content,
            info_type=InformationType.RUMOR,
            source=source,
            reliability=0.6,  # Rumors are less reliable
            importance=importance
        )
        self.add_information(info)
        return info
    
    def create_news(self, content: str, source: str, importance: int = 7) -> Information:
        """Helper to create and add news"""
        info = Information(
            content=content,
            info_type=InformationType.NEWS,
            source=source,
            reliability=0.9,  # News is more reliable
            importance=importance
        )
        self.add_information(info)
        return info
    
    def get_summary(self, npc_name: str) -> str:
        """Get summary of what NPC knows"""
        knowledge = self.get_recent_information(npc_name, 5)
        
        if not knowledge:
            return f"{npc_name} doesn't know much gossip."
        
        lines = [f"💬 {npc_name}'s Knowledge:"]
        for info in knowledge:
            reliability = "✓" if info.reliability > 0.7 else "?"
            lines.append(f"  {reliability} [{info.info_type.value}] {info.content}")
        
        return "\n".join(lines)
