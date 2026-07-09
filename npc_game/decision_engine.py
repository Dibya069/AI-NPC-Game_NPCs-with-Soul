"""
Decision Engine - Dynamic reasoning for NPCs
Includes: goal prioritizer, emotion state, and memory
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
import random


class EmotionType(Enum):
    """Types of emotions NPCs can experience"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    CURIOUS = "curious"
    AFRAID = "afraid"
    EXCITED = "excited"
    DISGUSTED = "disgusted"


@dataclass
class EmotionState:
    """Current emotional state of the NPC"""
    primary_emotion: EmotionType = EmotionType.NEUTRAL
    intensity: float = 0.0  # 0.0 to 1.0
    
    def update_emotion(self, new_emotion: EmotionType, intensity: float):
        """Update the emotional state"""
        self.primary_emotion = new_emotion
        self.intensity = max(0.0, min(1.0, intensity))
    
    def decay_emotion(self, decay_rate: float = 0.1):
        """Emotions naturally decay towards neutral"""
        self.intensity = max(0.0, self.intensity - decay_rate)
        if self.intensity < 0.2:
            self.primary_emotion = EmotionType.NEUTRAL
            self.intensity = 0.0
    
    def to_text(self) -> str:
        """Convert emotion to text description"""
        if self.intensity < 0.2:
            return "neutral"
        elif self.intensity < 0.5:
            return f"slightly {self.primary_emotion.value}"
        elif self.intensity < 0.8:
            return f"{self.primary_emotion.value}"
        else:
            return f"very {self.primary_emotion.value}"


@dataclass
class Goal:
    """A goal that the NPC wants to achieve"""
    description: str
    priority: int  # 1-10
    achieved: bool = False
    
    # Goal types: help, betray, ignore, investigate, etc.
    action_type: str = "neutral"


@dataclass
class MemoryEntry:
    """A single memory entry"""
    content: str
    turn: int
    importance: int  # 1-10
    emotional_impact: Optional[EmotionType] = None
    
    def to_text(self) -> str:
        """Convert memory to text"""
        text = f"Turn {self.turn}: {self.content}"
        if self.emotional_impact:
            text += f" (felt {self.emotional_impact.value})"
        return text


@dataclass
class Memory:
    """Memory system - both short-term and long-term"""
    
    # Short-term: recent interactions
    short_term: List[MemoryEntry] = field(default_factory=list)
    
    # Long-term: important memories stored in vector DB (simplified here)
    long_term: List[MemoryEntry] = field(default_factory=list)
    
    def add_memory(self, content: str, turn: int, importance: int = 5, 
                   emotional_impact: Optional[EmotionType] = None):
        """Add a new memory"""
        memory = MemoryEntry(
            content=content,
            turn=turn,
            importance=importance,
            emotional_impact=emotional_impact
        )
        
        # Add to short-term
        self.short_term.append(memory)
        
        # Important memories go to long-term
        if importance >= 7:
            self.long_term.append(memory)
    
    def get_recent_memories(self, count: int = 5) -> List[MemoryEntry]:
        """Get recent memories from short-term"""
        return sorted(self.short_term, key=lambda x: x.turn, reverse=True)[:count]
    
    def get_important_memories(self, threshold: int = 7) -> List[MemoryEntry]:
        """Get important memories"""
        return [m for m in self.long_term if m.importance >= threshold]
    
    def search_memories(self, keyword: str) -> List[MemoryEntry]:
        """Search memories by keyword"""
        all_memories = self.short_term + self.long_term
        return [m for m in all_memories if keyword.lower() in m.content.lower()]
    
    def get_memory_context(self) -> str:
        """Generate memory context for LLM"""
        context = "## Recent Memories:\n"
        recent = self.get_recent_memories(5)
        if recent:
            for mem in recent:
                context += f"- {mem.to_text()}\n"
        else:
            context += "- No recent memories\n"
        
        important = self.get_important_memories(8)
        if important:
            context += "\n## Important Past Memories:\n"
            for mem in important[-3:]:  # Last 3 important memories
                context += f"- {mem.to_text()}\n"
        
        return context
    
    def cleanup_old_memories(self, short_term_limit: int = 10):
        """Remove old short-term memories"""
        if len(self.short_term) > short_term_limit:
            # Keep recent and important
            self.short_term = sorted(self.short_term, key=lambda x: x.turn, reverse=True)[:short_term_limit]


@dataclass
class DecisionEngine:
    """
    The decision engine combines goals, emotions, and memories
    to determine NPC behavior
    """
    
    emotion_state: EmotionState = field(default_factory=EmotionState)
    memory: Memory = field(default_factory=Memory)
    current_goals: List[Goal] = field(default_factory=list)
    
    def add_goal(self, description: str, priority: int, action_type: str = "neutral"):
        """Add a new goal"""
        goal = Goal(description=description, priority=priority, action_type=action_type)
        self.current_goals.append(goal)
    
    def get_top_goal(self) -> Optional[Goal]:
        """Get the highest priority unachieved goal"""
        active_goals = [g for g in self.current_goals if not g.achieved]
        if not active_goals:
            return None
        return max(active_goals, key=lambda g: g.priority)
    
    def get_decision_context(self) -> str:
        """Generate decision context for LLM"""
        context = f"## Emotional State:\n{self.emotion_state.to_text()}\n\n"
        
        # Goals
        top_goal = self.get_top_goal()
        if top_goal:
            context += f"## Current Goal:\n{top_goal.description} (priority: {top_goal.priority})\n\n"
        
        # Memory context
        context += self.memory.get_memory_context()
        
        return context
