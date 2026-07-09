# AI NPC Game - Project Overview

## What is this?

An advanced AI-powered NPC (Non-Player Character) system where game characters have their own "soul" - complete with:
- 🎭 **Dynamic personalities** that shape every interaction
- 🧠 **Memory systems** that remember past conversations
- 😊 **Emotional states** that change based on how you treat them
- 🎯 **Personal goals** they're trying to achieve
- 🤝 **Relationship tracking** (they'll trust or distrust you)
- 🔒 **Secrets** they won't reveal unless they trust you

## Architecture

The system implements the architecture from your image:

```
┌─────────────────────────────────────────────────────────┐
│  Single NPC - AI Brain (All components run per NPC)    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🟢 PERSONA CORE (Static Identity)                     │
│     ├─ Traits (brave, greedy, loyal)                   │
│     ├─ Backstory (past events, wounds)                 │
│     ├─ Core Motive (wants power/love/safety)           │
│     ├─ Beliefs (worldview, biases)                     │
│     └─ Secrets (hidden from player)                    │
│                         ↓                               │
│  🟠 PERCEPTION LAYER (What NPC observes)               │
│     ├─ Player words + tone (friendly/aggressive)       │
│     └─ World events + NPC gossip                       │
│                         ↓                               │
│  🟠 DECISION ENGINE (Dynamic reasoning)                │
│     ├─ Goal prioritizer (rank wants vs needs)          │
│     ├─ Emotion state (angry, curious, afraid)          │
│     └─ Memory (short-term + long-term)                 │
│                         ↓                               │
│  🟣 LLM + OUTPUT (Generates response)                  │
│     ├─ Context window (persona + memory +)             │
│     ├─ Dialogue reply (voice, tone, accent)            │
│     ├─ Action intent (help/betray/ignore)              │
│     ├─ Relationship delta (trust +/- update)           │
│     └─ Memory write (store this interaction)           │
└─────────────────────────────────────────────────────────┘
```

## Files Structure

```
npc_game/                   # Main package
├── __init__.py            # Package initialization
├── config.py              # Configuration (memory limits, etc.)
├── persona_core.py        # 🟢 Persona system (traits, backstory, etc.)
├── perception.py          # 🟠 Perception layer (observations, tone)
├── decision_engine.py     # 🟠 Goals, emotions, memory
├── llm_integration.py     # 🟣 Groq API integration
├── npc.py                 # Main NPC class (combines all layers)
└── game.py                # Game loop and world management

main.py                    # ▶️  Interactive game (start here!)
demo.py                    # 🧪 Quick test/demo script
example_usage.py           # 📚 Detailed code examples
README.md                  # 📖 Full documentation
QUICKSTART.md              # 🚀 5-minute setup guide
PROJECT_OVERVIEW.md        # 📋 This file
```

## Quick Start

### 1. Install
```bash
pip install groq
```

### 2. Get API Key
Visit https://console.groq.com/ and get a free API key

### 3. Set Environment Variable
```bash
export GROQ_API_KEY='your-key-here'
```

### 4. Run
```bash
# Quick test
python demo.py

# Interactive game
python main.py

# See examples
python example_usage.py
```

## Pre-made NPCs

### 🍺 Greta the Tavern Keeper
- **Traits**: Jovial, gossipy, greedy, protective
- **Motive**: Keep tavern profitable, know everyone's business
- **Secrets**: Waters down wine, involved in smuggling
- **Relationships**: Bribes the mayor, friends with guard captain

### 🔮 Aldric the Scholar
- **Traits**: Brilliant, paranoid, obsessive, socially awkward
- **Motive**: Prove forbidden magic theories at any cost
- **Secrets**: Summoned something dangerous, stole forbidden books
- **Relationships**: Hates the Academy, haunted by mentor's disappointment

### ⚔️ Captain Thorne
- **Traits**: Honorable, stern, duty-bound, secretly weary
- **Motive**: Protect innocents, dreams of retiring
- **Secrets**: Overwhelmed, turning blind eye to minor crimes
- **Relationships**: Distrusts corrupt mayor, old friends with Greta

## How NPCs "Think"

Every time you interact with an NPC:

1. **Perception**: Analyzes your words and tone
2. **Emotion Update**: Their mood changes (anger, happiness, fear, etc.)
3. **Context Building**: Combines:
   - Who they are (persona)
   - How they feel (emotion)
   - What they remember (memory)
   - What they want (goals)
   - How they feel about you (relationship)
4. **LLM Generation**: Groq AI generates in-character response
5. **Memory Storage**: Stores this conversation for future reference
6. **Relationship Update**: Trust level changes based on interaction

## Key Features

✨ **Living NPCs**: Each has unique personality that affects all responses  
🧠 **Persistent Memory**: NPCs remember what you said 10 turns ago  
😊 **Dynamic Emotions**: Be rude, they get angry. Be kind, they warm up  
🎯 **Goal-Oriented**: NPCs pursue their own objectives  
🤝 **Relationship System**: Build trust over time to learn secrets  
🔒 **Secret Keeper**: NPCs won't reveal everything immediately  
⚡ **Fast**: Powered by Groq's ultra-fast LLM inference  

## Example Interaction

```python
from npc_game.persona_core import create_tavern_keeper
from npc_game.npc import NPC
from npc_game.llm_integration import GroqLLMClient
import os

# Create NPC
greta = NPC(persona=create_tavern_keeper())
greta.llm_client = GroqLLMClient(api_key=os.getenv('GROQ_API_KEY'))

# Talk to her
response = greta.interact("What's the best drink here?")
print(response)
# Output: "Ah, if you've got the coin, our Golden Mead is legendary!"

# Check her status
print(f"Emotion: {greta.decision_engine.emotion_state.to_text()}")
print(f"Trust: {greta.player_trust}/100")
```

## Customization

### Create Your Own NPC
```python
from npc_game.persona_core import PersonaCore

my_npc = PersonaCore(
    name="Your Character",
    occupation="Their job",
    traits=["personality", "traits"],
    backstory="Their history...",
    core_motive="What they want",
    beliefs=["What they believe"],
    secrets=["Hidden truths"]
)
```

## Future Ideas

- 🗄️ Vector database for better long-term memory
- 🌍 Persistent world that saves state
- 👥 NPC-to-NPC conversations
- 📊 Visual relationship graphs
- 🎨 Web-based GUI
- 🔊 Voice synthesis
- 🎲 RPG stat integration

## Tech Stack

- **Language**: Python 3.7+
- **LLM**: Groq (Llama 3.3 70B)
- **Architecture**: Modular, extensible design
- **Memory**: Short-term + long-term dual system
- **Emotions**: 8 base emotions with intensity
- **Relationships**: -100 to +100 trust scale

## Credits

Based on advanced NPC AI architecture principles.  
Powered by Groq's lightning-fast LLM API.

---

**Ready to create NPCs with soul?** 🎭✨

Start with: `python demo.py`
