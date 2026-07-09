"""
NPC-to-NPC Interactions
Allows NPCs to talk to each other, share gossip, and build relationships
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from .npc import NPC
from .decision_engine import EmotionType
from .llm_integration import build_system_prompt


@dataclass
class NPCConversation:
    """Represents a conversation between two NPCs"""
    npc1_name: str
    npc2_name: str
    turns: List[Tuple[str, str]] = field(default_factory=list)  # (speaker, message)
    turn_count: int = 0
    
    def add_turn(self, speaker: str, message: str):
        """Add a turn to the conversation"""
        self.turns.append((speaker, message))
        self.turn_count += 1
    
    def get_last_n_turns(self, n: int = 3) -> List[Tuple[str, str]]:
        """Get the last N turns"""
        return self.turns[-n:]
    
    def get_summary(self) -> str:
        """Get a summary of the conversation"""
        summary = f"Conversation between {self.npc1_name} and {self.npc2_name}:\n"
        for speaker, message in self.turns:
            summary += f"[{speaker}]: {message}\n"
        return summary


class NPCInteractionManager:
    """
    Manages NPC-to-NPC interactions
    """
    
    def __init__(self):
        self.active_conversations: Dict[str, NPCConversation] = {}
        self.gossip_network: List[str] = []  # Shared gossip
        self.npc_relationships: Dict[str, Dict[str, int]] = {}  # npc1 -> npc2 -> relationship_score
    
    def get_conversation_key(self, npc1_name: str, npc2_name: str) -> str:
        """Get a unique key for a conversation"""
        names = sorted([npc1_name, npc2_name])
        return f"{names[0]}<->{names[1]}"
    
    def start_conversation(self, npc1: NPC, npc2: NPC, topic: Optional[str] = None) -> NPCConversation:
        """
        Start a conversation between two NPCs
        
        Args:
            npc1: First NPC
            npc2: Second NPC
            topic: Optional topic to discuss
            
        Returns:
            NPCConversation object
        """
        key = self.get_conversation_key(npc1.persona.name, npc2.persona.name)
        
        if key not in self.active_conversations:
            self.active_conversations[key] = NPCConversation(
                npc1_name=npc1.persona.name,
                npc2_name=npc2.persona.name
            )
        
        return self.active_conversations[key]
    
    def npc_to_npc_exchange(self, npc1: NPC, npc2: NPC, topic: str, turns: int = 3) -> NPCConversation:
        """
        Simulate a conversation between two NPCs
        
        Args:
            npc1: First NPC (initiates)
            npc2: Second NPC (responds)
            topic: What they're discussing
            turns: Number of back-and-forth exchanges
            
        Returns:
            NPCConversation with the full exchange
        """
        conversation = self.start_conversation(npc1, npc2)
        
        # Get their existing relationship
        rel_score = self.get_relationship(npc1.persona.name, npc2.persona.name)
        
        # NPC1 starts the conversation
        current_topic = topic
        
        for i in range(turns):
            # NPC1 speaks
            if i == 0:
                # Opening statement
                prompt1 = self._build_npc_to_npc_prompt(
                    npc1, npc2, current_topic, conversation, rel_score, is_initiator=True
                )
            else:
                # Response to NPC2's last message
                prompt1 = self._build_npc_to_npc_prompt(
                    npc1, npc2, current_topic, conversation, rel_score, is_initiator=False
                )
            
            if npc1.llm_client:
                response1 = npc1.llm_client.generate_npc_response(prompt1)
                # Extract just the dialogue
                if "DIALOGUE:" in response1:
                    dialogue1 = response1.split("DIALOGUE:")[1].split("\n")[0].strip()
                else:
                    dialogue1 = response1.strip()
            else:
                dialogue1 = f"{npc1.persona.name} speaks about {current_topic}"
            
            conversation.add_turn(npc1.persona.name, dialogue1)
            
            # NPC2 responds
            prompt2 = self._build_npc_to_npc_prompt(
                npc2, npc1, current_topic, conversation, rel_score, is_initiator=False
            )
            
            if npc2.llm_client:
                response2 = npc2.llm_client.generate_npc_response(prompt2)
                if "DIALOGUE:" in response2:
                    dialogue2 = response2.split("DIALOGUE:")[1].split("\n")[0].strip()
                else:
                    dialogue2 = response2.strip()
            else:
                dialogue2 = f"{npc2.persona.name} responds"
            
            conversation.add_turn(npc2.persona.name, dialogue2)
        
        # Update both NPCs' memories about this conversation
        self._update_npc_memories_after_conversation(npc1, npc2, conversation)
        
        # Extract any gossip from the conversation
        self._extract_gossip_from_conversation(conversation)
        
        return conversation
    
    def _build_npc_to_npc_prompt(self, speaker: NPC, listener: NPC, topic: str, 
                                  conversation: NPCConversation, relationship: int,
                                  is_initiator: bool) -> str:
        """Build a prompt for NPC-to-NPC dialogue"""
        
        persona_summary = speaker.persona.get_persona_summary()
        
        prompt = f"""You are {speaker.persona.name} talking to {listener.persona.name} (another NPC).

{persona_summary}

## About {listener.persona.name}:
Occupation: {listener.persona.occupation}
Your relationship with them: {relationship}/100 ({self._relationship_description(relationship)})

## Conversation Topic:
{topic}

## Conversation So Far:
"""
        
        recent_turns = conversation.get_last_n_turns(3)
        if recent_turns:
            for speaker_name, message in recent_turns:
                prompt += f"[{speaker_name}]: {message}\n"
        else:
            prompt += "This is the start of the conversation.\n"
        
        if is_initiator:
            prompt += f"\nYou are bringing up the topic: {topic}\n"
        
        prompt += """
Respond as your character. Keep it natural and conversational (1-2 sentences).
You're talking to another NPC, not the player.

DIALOGUE: """
        
        return prompt
    
    def _update_npc_memories_after_conversation(self, npc1: NPC, npc2: NPC, conversation: NPCConversation):
        """Update both NPCs' memories after they talk"""
        summary = f"Had a conversation with {npc2.persona.name}"
        npc1.decision_engine.memory.add_memory(
            content=summary,
            turn=npc1.current_turn,
            importance=6
        )
        
        summary = f"Had a conversation with {npc1.persona.name}"
        npc2.decision_engine.memory.add_memory(
            content=summary,
            turn=npc2.current_turn,
            importance=6
        )
    
    def _extract_gossip_from_conversation(self, conversation: NPCConversation):
        """Extract gossip from NPC conversations and add to gossip network"""
        # Simple heuristic: if conversation mentions certain keywords, it becomes gossip
        gossip_keywords = ['secret', 'heard', 'saw', 'suspicious', 'rumor', 'strange']
        
        for speaker, message in conversation.turns:
            if any(keyword in message.lower() for keyword in gossip_keywords):
                gossip = f"{speaker} mentioned: {message}"
                if gossip not in self.gossip_network:
                    self.gossip_network.append(gossip)
    
    def get_relationship(self, npc1_name: str, npc2_name: str) -> int:
        """Get relationship score between two NPCs"""
        if npc1_name not in self.npc_relationships:
            return 0
        return self.npc_relationships[npc1_name].get(npc2_name, 0)
    
    def update_relationship(self, npc1_name: str, npc2_name: str, delta: int):
        """Update relationship between two NPCs"""
        if npc1_name not in self.npc_relationships:
            self.npc_relationships[npc1_name] = {}
        
        current = self.npc_relationships[npc1_name].get(npc2_name, 0)
        self.npc_relationships[npc1_name][npc2_name] = max(-100, min(100, current + delta))
    
    def _relationship_description(self, score: int) -> str:
        """Convert relationship score to description"""
        if score > 50:
            return "close friends"
        elif score > 20:
            return "friendly"
        elif score > -20:
            return "neutral"
        elif score > -50:
            return "unfriendly"
        else:
            return "hostile"
    
    def spread_gossip_to_npc(self, npc: NPC, count: int = 2):
        """Share recent gossip with an NPC"""
        if not self.gossip_network:
            return
        
        # Give NPC the latest gossip
        recent_gossip = self.gossip_network[-count:]
        for gossip in recent_gossip:
            npc.perception.learn_gossip(gossip)
