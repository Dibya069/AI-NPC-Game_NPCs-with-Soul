"""
LLM Integration - Groq API integration for NPC dialogue and reasoning
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass


# Import Groq client
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("Warning: Groq library not installed. Install with: pip install groq")


@dataclass
class LLMResponse:
    """Response from the LLM"""
    dialogue: str  # What the NPC says
    internal_thoughts: str  # NPC's reasoning (not shown to player)
    action_intent: str  # help, betray, ignore, investigate, etc.
    emotion_change: Optional[str] = None  # New emotion if any
    relationship_delta: int = 0  # Change in relationship trust (-10 to +10)


class GroqLLMClient:
    """
    Groq LLM client for generating NPC responses
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Groq client"""
        if not GROQ_AVAILABLE:
            raise ImportError("Groq library not installed")
        
        self.api_key = api_key or os.getenv('GROQ_API_KEY', '')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not set. Set it as environment variable or pass to constructor.")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
        self.temperature = 0.7  # Higher for more creative/varied responses
    
    def generate_npc_response(self, system_prompt: str) -> str:
        """
        Generate NPC response using Groq
        
        Args:
            system_prompt: The complete context and prompt for the NPC
            
        Returns:
            The LLM's response text
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": system_prompt}
                ],
                model=self.model,
                temperature=self.temperature
            )
            
            output = chat_completion.choices[0].message.content
            return output
        
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return "I seem to be at a loss for words..."
    
    def parse_response(self, llm_output: str) -> LLMResponse:
        """
        Parse the LLM output into structured response
        Expected format:
        DIALOGUE: <what NPC says>
        THOUGHTS: <internal reasoning>
        ACTION: <help/betray/ignore/investigate>
        EMOTION: <optional emotion change>
        TRUST: <optional relationship change>
        """
        dialogue = ""
        thoughts = ""
        action = "neutral"
        emotion = None
        trust_delta = 0
        
        lines = llm_output.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('DIALOGUE:'):
                dialogue = line.replace('DIALOGUE:', '').strip()
            elif line.startswith('THOUGHTS:'):
                thoughts = line.replace('THOUGHTS:', '').strip()
            elif line.startswith('ACTION:'):
                action = line.replace('ACTION:', '').strip().lower()
            elif line.startswith('EMOTION:'):
                emotion = line.replace('EMOTION:', '').strip().lower()
            elif line.startswith('TRUST:'):
                try:
                    trust_delta = int(line.replace('TRUST:', '').strip())
                except ValueError:
                    trust_delta = 0
        
        # If dialogue not found with format, use entire output as dialogue
        if not dialogue:
            dialogue = llm_output.strip()
        
        return LLMResponse(
            dialogue=dialogue,
            internal_thoughts=thoughts,
            action_intent=action,
            emotion_change=emotion,
            relationship_delta=trust_delta
        )


def build_system_prompt(persona_summary: str, perception_context: str, 
                       decision_context: str, player_input: str,
                       relationship_level: int = 0) -> str:
    """
    Build the complete system prompt for the LLM
    
    Args:
        persona_summary: The NPC's persona core summary
        perception_context: What the NPC observes
        decision_context: Goals, emotions, memories
        player_input: What the player just said/did
        relationship_level: Current trust level with player (-100 to +100)
    
    Returns:
        Complete system prompt
    """
    
    trust_description = "neutral"
    if relationship_level > 50:
        trust_description = "trusted friend"
    elif relationship_level > 20:
        trust_description = "friendly acquaintance"
    elif relationship_level < -50:
        trust_description = "hated enemy"
    elif relationship_level < -20:
        trust_description = "distrusted person"
    
    prompt = f"""You are roleplaying as an NPC in a fantasy game. You must stay in character at all times.

{persona_summary}

{perception_context}

{decision_context}

## Relationship with Player:
Current trust level: {relationship_level}/100 ({trust_description})

## Player's Current Action:
{player_input}

## Your Task:
Respond to the player AS THIS CHARACTER. Consider:
1. Your personality traits and beliefs
2. Your current emotional state
3. Your goals and motivations
4. Your memories of past interactions
5. Your secrets (which you won't reveal easily)

IMPORTANT: You can and should TAKE ACTION when appropriate:
- If threatened or insulted severely, you might: call guards, flee, attack, or confront them
- If told shocking news about another NPC, you might: investigate, confront that NPC immediately
- If someone confesses to a crime, guards should arrest them or be suspicious
- Don't just keep talking - ACT when your character would realistically do something!

Format your response as follows:
DIALOGUE: <What you say to the player - keep it natural and in-character>
THOUGHTS: <Your internal reasoning - why you're responding this way>
ACTION: <Your intent: help/betray/ignore/investigate/neutral/flee/call_guards/confront/attack>
EMOTION: <Your new emotion if it changes: happy/sad/angry/curious/afraid/excited/disgusted/neutral>
TRUST: <Change in trust toward player: -10 to +10>

Stay in character. Be creative and dynamic. TAKE ACTION when your character realistically would!
"""
    
    return prompt
