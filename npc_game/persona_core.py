"""
Persona Core - The static identity of an NPC
Includes: traits, backstory, core motive, beliefs, and secrets
"""

from typing import List, Dict
from dataclasses import dataclass, field


@dataclass
class PersonaCore:
    """
    The core identity of an NPC that defines who they are.
    This is static and doesn't change during gameplay.
    """
    
    name: str
    
    # Traits: personality characteristics
    traits: List[str] = field(default_factory=list)
    
    # Backstory: past events and wounds
    backstory: str = ""
    
    # Core Motive: what they want (power, love, safety, etc.)
    core_motive: str = ""
    
    # Beliefs: worldview and biases
    beliefs: List[str] = field(default_factory=list)
    
    # Secrets: hidden from the player
    secrets: List[str] = field(default_factory=list)
    
    # Occupation/role
    occupation: str = ""
    
    # Relationships with other NPCs
    relationships: Dict[str, str] = field(default_factory=dict)
    
    def get_persona_summary(self) -> str:
        """Generate a text summary of the persona for LLM context"""
        summary = f"Character: {self.name}\n"
        summary += f"Occupation: {self.occupation}\n"
        summary += f"Traits: {', '.join(self.traits)}\n"
        summary += f"Core Motive: {self.core_motive}\n"
        summary += f"Backstory: {self.backstory}\n"
        summary += f"Beliefs: {', '.join(self.beliefs)}\n"
        
        if self.relationships:
            summary += "Relationships:\n"
            for person, relationship in self.relationships.items():
                summary += f"  - {person}: {relationship}\n"
        
        return summary
    
    def get_secrets_summary(self) -> str:
        """Get secrets (not shared with player, but used for NPC reasoning)"""
        if not self.secrets:
            return ""
        return "Secrets (hidden from player): " + ", ".join(self.secrets)


# Example persona templates
def create_tavern_keeper() -> PersonaCore:
    """Create a tavern keeper NPC"""
    return PersonaCore(
        name="Greta the Tavern Keeper",
        occupation="Tavern Owner",
        traits=["jovial", "gossipy", "greedy", "protective of regulars"],
        backstory="Greta inherited the Silver Mug tavern from her father. She's seen countless adventurers come and go, and knows everyone's business in town.",
        core_motive="Wants to keep her tavern profitable and be the center of town gossip",
        beliefs=[
            "Money talks",
            "A good ale can solve most problems",
            "Strangers are either customers or trouble"
        ],
        secrets=[
            "She's been watering down the expensive wine",
            "She knows about the smuggling ring but stays quiet for a cut"
        ],
        relationships={
            "Mayor Thornwell": "Pays him bribes to ignore health violations",
            "Guard Captain": "Old flame, still friendly"
        }
    )


def create_mysterious_scholar() -> PersonaCore:
    """Create a mysterious scholar NPC"""
    return PersonaCore(
        name="Aldric the Scholar",
        occupation="Arcane Researcher",
        traits=["brilliant", "paranoid", "obsessive", "socially awkward"],
        backstory="Aldric was expelled from the Mage's Academy for forbidden research. Now he works in isolation, seeking knowledge others fear.",
        core_motive="Wants to prove his theories about ancient magic, regardless of the cost",
        beliefs=[
            "Knowledge is worth any price",
            "The Academy are cowards and fools",
            "Magic should have no restrictions"
        ],
        secrets=[
            "He's accidentally summoned something dangerous",
            "He stole several forbidden tomes from the Academy"
        ],
        relationships={
            "The Academy": "Bitter enemies, wants revenge",
            "His mentor": "Deceased, haunted by their disappointment"
        }
    )


def create_guard_captain() -> PersonaCore:
    """Create a guard captain NPC"""
    return PersonaCore(
        name="Captain Thorne",
        occupation="City Guard Captain",
        traits=["honorable", "stern", "duty-bound", "secretly weary"],
        backstory="Thorne has served the city for 20 years. He's seen too much violence and corruption, but duty keeps him at his post.",
        core_motive="Wants to protect the innocent and maintain order, dreams of retiring to a quiet farm",
        beliefs=[
            "Law and order must be maintained",
            "Everyone deserves a fair trial",
            "Corruption is a cancer that must be cut out"
        ],
        secrets=[
            "He's turning a blind eye to minor crimes because he's overwhelmed",
            "He's planning to retire soon but hasn't told anyone"
        ],
        relationships={
            "Mayor": "Distrusts him, suspects corruption",
            "Greta": "Old friend from better days"
        }
    )
