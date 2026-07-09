"""
NPC - The complete NPC with all components integrated
"""

from typing import Optional
from dataclasses import dataclass, field

from .persona_core import PersonaCore
from .perception import PerceptionLayer, Tone, analyze_player_tone
from .decision_engine import DecisionEngine, EmotionType
from .llm_integration import GroqLLMClient, build_system_prompt, LLMResponse


@dataclass
class NPC:
    """
    A complete NPC with personality, perception, decision-making, and LLM-powered dialogue
    """
    
    # Core components
    persona: PersonaCore
    perception: PerceptionLayer = field(default_factory=PerceptionLayer)
    decision_engine: DecisionEngine = field(default_factory=DecisionEngine)
    
    # LLM client
    llm_client: Optional[GroqLLMClient] = None
    
    # Relationship with player
    player_trust: int = 0  # -100 to +100
    
    # Turn counter
    current_turn: int = 0
    
    def __post_init__(self):
        """Initialize the NPC"""
        # Set initial goal based on core motive
        if self.persona.core_motive:
            self.decision_engine.add_goal(
                description=self.persona.core_motive,
                priority=8,
                action_type="neutral"
            )
    
    def interact(self, player_input: str) -> str:
        """
        Main interaction method - player says something, NPC responds
        
        Args:
            player_input: What the player said or did
            
        Returns:
            The NPC's dialogue response
        """
        self.current_turn += 1
        
        # 1. PERCEPTION: Analyze and observe player input
        tone = analyze_player_tone(player_input)
        self.perception.observe_player_action(player_input, tone, self.current_turn)
        
        # 2. DECISION ENGINE: Process the observation
        # Emotion might change based on tone
        if tone == Tone.AGGRESSIVE:
            self.decision_engine.emotion_state.update_emotion(EmotionType.ANGRY, 0.7)
        elif tone == Tone.FRIENDLY:
            self.decision_engine.emotion_state.update_emotion(EmotionType.HAPPY, 0.5)
        elif tone == Tone.PLEADING:
            if self.player_trust > 0:
                self.decision_engine.emotion_state.update_emotion(EmotionType.CURIOUS, 0.6)
            else:
                self.decision_engine.emotion_state.update_emotion(EmotionType.DISGUSTED, 0.4)
        
        # 3. LLM: Generate response
        if self.llm_client:
            response = self._generate_llm_response(player_input)
        else:
            response = self._generate_fallback_response(player_input)
        
        # 4. MEMORY: Store this interaction
        self.decision_engine.memory.add_memory(
            content=f"Player: '{player_input}' | I responded: '{response.dialogue}'",
            turn=self.current_turn,
            importance=5,
            emotional_impact=self.decision_engine.emotion_state.primary_emotion
        )
        
        # 5. Update relationship based on response
        self.player_trust = max(-100, min(100, self.player_trust + response.relationship_delta))

        # 6. Handle action intent (what NPC wants to do)
        action_message = ""
        if response.action_intent and response.action_intent != "neutral":
            action_message = self._handle_action_intent(response.action_intent, player_input)

        # 7. Cleanup old data
        self.perception.clear_old_observations(keep_recent=10)
        self.decision_engine.memory.cleanup_old_memories(short_term_limit=10)

        # 8. Emotion decay
        self.decision_engine.emotion_state.decay_emotion(0.1)

        # Return dialogue + action if any
        full_response = response.dialogue
        if action_message:
            full_response += f"\n\n{action_message}"

        return full_response
    
    def _generate_llm_response(self, player_input: str) -> LLMResponse:
        """Generate response using LLM"""
        # Build the system prompt with all context
        persona_summary = self.persona.get_persona_summary()
        secrets_summary = self.persona.get_secrets_summary()
        full_persona = persona_summary + "\n" + secrets_summary
        
        perception_context = self.perception.get_perception_context()
        decision_context = self.decision_engine.get_decision_context()
        
        system_prompt = build_system_prompt(
            persona_summary=full_persona,
            perception_context=perception_context,
            decision_context=decision_context,
            player_input=player_input,
            relationship_level=self.player_trust
        )
        
        # Call LLM
        llm_output = self.llm_client.generate_npc_response(system_prompt)
        
        # Parse response
        response = self.llm_client.parse_response(llm_output)
        
        # Update emotion if specified
        if response.emotion_change:
            try:
                new_emotion = EmotionType(response.emotion_change)
                self.decision_engine.emotion_state.update_emotion(new_emotion, 0.7)
            except ValueError:
                pass  # Invalid emotion, ignore
        
        return response
    
    def _generate_fallback_response(self, player_input: str) -> LLMResponse:
        """Fallback response when LLM is not available"""
        return LLMResponse(
            dialogue=f"{self.persona.name} nods thoughtfully.",
            internal_thoughts="No LLM available",
            action_intent="neutral",
            relationship_delta=0
        )

    def _handle_action_intent(self, action: str, player_input: str) -> str:
        """
        Handle NPC action intents - what they actually DO

        Args:
            action: The action intent (help, betray, investigate, flee, etc.)
            player_input: What the player said

        Returns:
            A message describing what the NPC does
        """
        action = action.lower()

        if action == "flee":
            return f"💨 [{self.persona.name} quickly leaves the area, looking scared]"

        elif action == "investigate":
            return f"🔍 [{self.persona.name} looks around suspiciously, clearly planning to investigate this matter]"

        elif action == "help":
            return f"🤝 [{self.persona.name} seems genuinely willing to help you]"

        elif action == "betray":
            return f"⚠️  [{self.persona.name}'s eyes narrow - you sense they might betray you]"

        elif action == "ignore":
            return f"🙄 [{self.persona.name} dismisses you and turns away]"

        elif action == "call_guards" or "alert" in action:
            if "guard" in self.persona.occupation.lower() or "captain" in self.persona.occupation.lower():
                return f"⚔️  [{self.persona.name} puts hand on weapon, ready for action]"
            else:
                return f"🚨 [{self.persona.name} shouts for the guards!]"

        elif action == "attack" or action == "fight":
            return f"⚔️  [{self.persona.name} reaches for a weapon, ready to fight!]"

        elif "confront" in action or "investigate" in action:
            # Extract who they want to confront from the player input
            other_npcs = ["Greta", "Aldric", "Thorne", "Captain"]
            mentioned = [npc for npc in other_npcs if npc.lower() in player_input.lower()]
            if mentioned:
                return f"🚶 [{self.persona.name} immediately heads off to confront {mentioned[0]}]"
            else:
                return f"🚶 [{self.persona.name} heads off to investigate the matter]"

        # Default - show they're considering it
        return f"💭 [{self.persona.name} seems to be considering their next move...]"

    def get_status(self) -> str:
        """Get a status summary of the NPC"""
        status = f"\n--- {self.persona.name} ---\n"
        status += f"Emotion: {self.decision_engine.emotion_state.to_text()}\n"
        status += f"Trust level: {self.player_trust}/100\n"

        top_goal = self.decision_engine.get_top_goal()
        if top_goal:
            status += f"Current goal: {top_goal.description}\n"

        return status
