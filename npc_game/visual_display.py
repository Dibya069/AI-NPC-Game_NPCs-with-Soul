"""
Visual Display - Rich terminal UI for NPC status and game state
"""

from typing import Dict, List, Optional
from .npc import NPC
from .world_events import WorldEvent


class VisualDisplay:
    """
    Create rich terminal displays for game state
    """
    
    @staticmethod
    def create_box(content: str, width: int = 60, title: str = "") -> str:
        """Create a box around content"""
        lines = content.split('\n')
        
        result = "┌" + "─" * (width - 2) + "┐\n"
        
        if title:
            title_line = f"│ {title}" + " " * (width - len(title) - 3) + "│\n"
            result += title_line
            result += "├" + "─" * (width - 2) + "┤\n"
        
        for line in lines:
            # Truncate or pad line to fit
            if len(line) > width - 4:
                line = line[:width - 7] + "..."
            padded = f"│ {line}" + " " * (width - len(line) - 3) + "│\n"
            result += padded
        
        result += "└" + "─" * (width - 2) + "┘"
        return result
    
    @staticmethod
    def show_npc_card(npc: NPC, show_secrets: bool = False) -> str:
        """Create a detailed NPC status card"""
        width = 70
        
        # Emotion bar
        emotion = npc.decision_engine.emotion_state
        emotion_text = emotion.to_text()
        
        # Trust bar
        trust = npc.player_trust
        trust_bars = int((trust + 100) / 20)  # 0-10 bars
        trust_visual = "█" * trust_bars + "░" * (10 - trust_bars)
        
        # Build content
        content = f"""
╔══════════════════════════════════════════════════════════════════╗
║  {npc.persona.name:^62}  ║
╠══════════════════════════════════════════════════════════════════╣
║  Role: {npc.persona.occupation:<56} ║
║  Traits: {', '.join(npc.persona.traits[:3]):<53} ║
╠══════════════════════════════════════════════════════════════════╣
║  😊 Emotion: {emotion_text:<50} ║
║  🤝 Trust: {trust_visual} ({trust:+4d}/100)                        ║
╠══════════════════════════════════════════════════════════════════╣
"""
        
        # Current goal
        top_goal = npc.decision_engine.get_top_goal()
        if top_goal:
            goal_text = top_goal.description[:55]
            content += f"║  🎯 Goal: {goal_text:<55} ║\n"
        
        # Recent memories
        recent_memories = npc.decision_engine.memory.get_recent_memories(2)
        if recent_memories:
            content += "║  🧠 Recent Memories:                                            ║\n"
            for mem in recent_memories:
                mem_text = mem.content[:60]
                content += f"║     • {mem_text:<58} ║\n"
        
        # Known gossip
        if npc.perception.known_gossip:
            content += "║  💬 Known Gossip:                                               ║\n"
            for gossip in npc.perception.known_gossip[-2:]:
                gossip_text = gossip[:60]
                content += f"║     • {gossip_text:<58} ║\n"
        
        # Secrets (if showing)
        if show_secrets and npc.persona.secrets:
            content += "╠══════════════════════════════════════════════════════════════════╣\n"
            content += "║  🔒 SECRETS (Hidden from player):                               ║\n"
            for secret in npc.persona.secrets[:2]:
                secret_text = secret[:60]
                content += f"║     • {secret_text:<58} ║\n"
        
        content += "╚══════════════════════════════════════════════════════════════════╝"
        
        return content
    
    @staticmethod
    def show_world_status(events: List[WorldEvent], turn: int) -> str:
        """Show current world status"""
        content = f"""
╔══════════════════════════════════════════════════════════════════╗
║  🌍 WORLD STATUS - Turn {turn:<47} ║
╠══════════════════════════════════════════════════════════════════╣
"""
        
        if events:
            content += "║  Recent Events:                                                 ║\n"
            for event in events[-3:]:
                event_text = f"{event.name}: {event.description}"[:60]
                content += f"║  • {event_text:<61} ║\n"
        else:
            content += "║  No recent events                                               ║\n"
        
        content += "╚══════════════════════════════════════════════════════════════════╝"
        
        return content
    
    @staticmethod
    def show_relationship_network(npcs: Dict[str, NPC], relationships: Dict[str, Dict[str, int]]) -> str:
        """Show relationships between NPCs"""
        content = """
╔══════════════════════════════════════════════════════════════════╗
║  👥 NPC RELATIONSHIP NETWORK                                     ║
╠══════════════════════════════════════════════════════════════════╣
"""
        
        npc_names = list(npcs.keys())
        
        for i, npc1_name in enumerate(npc_names):
            for npc2_name in npc_names[i+1:]:
                # Get relationship
                rel1 = relationships.get(npc1_name, {}).get(npc2_name, 0)
                rel2 = relationships.get(npc2_name, {}).get(npc1_name, 0)
                
                # Average relationship
                avg_rel = (rel1 + rel2) // 2
                
                # Visualize
                if avg_rel > 20:
                    symbol = "💚"
                    desc = "friendly"
                elif avg_rel < -20:
                    symbol = "💔"
                    desc = "hostile"
                else:
                    symbol = "🤝"
                    desc = "neutral"
                
                # Shorten names
                name1_short = npc1_name.split()[0]
                name2_short = npc2_name.split()[0]
                
                line = f"{symbol} {name1_short} ↔ {name2_short}: {desc} ({avg_rel:+d})"
                content += f"║  {line:<64} ║\n"
        
        content += "╚══════════════════════════════════════════════════════════════════╝"
        
        return content
    
    @staticmethod
    def show_conversation_history(npc: NPC, count: int = 5) -> str:
        """Show conversation history with an NPC"""
        memories = npc.decision_engine.memory.get_recent_memories(count)
        
        content = f"""
╔══════════════════════════════════════════════════════════════════╗
║  💬 Conversation History with {npc.persona.name:<33} ║
╠══════════════════════════════════════════════════════════════════╣
"""
        
        if memories:
            for mem in reversed(memories):
                mem_text = mem.content[:62]
                content += f"║ Turn {mem.turn:>3}: {mem_text:<54} ║\n"
        else:
            content += "║  No conversation history yet                                    ║\n"
        
        content += "╚══════════════════════════════════════════════════════════════════╝"
        
        return content
