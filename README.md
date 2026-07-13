# AI NPC Game - NPCs with Soul 🎮🤖

An advanced AI-powered NPC system where game characters have their own "soul" - complete with dynamic personalities, memories, emotions, and decision-making powered by LLMs.

## Architecture

Based on the architecture from the diagram, each NPC consists of three main layers:

### 🟢 Persona Core (Static Identity)
- **Traits**: Personality characteristics (brave, greedy, loyal, etc.)
- **Backstory**: Past events and emotional wounds
- **Core Motive**: What they want (power, love, safety, revenge)
- **Beliefs**: Worldview and biases
- **Secrets**: Hidden information not revealed to players

### 🟠 Perception Layer (What NPCs Observe)
- **Player Words + Tone**: Analyzes what players say and how they say it
- **World Events**: Observes changes in the game world
- **NPC Gossip**: Hears rumors and information from other NPCs

### 🔴 Decision Engine (Dynamic Reasoning)
- **Goal Prioritizer**: Ranks wants vs needs
- **Emotion State**: Tracks anger, curiosity, fear, etc.
- **Memory System**:
  - Short-term: Recent interactions (last 5-10 turns)
  - Long-term: Important events stored for recall

### 🟣 LLM + Output (Response Generation)
- **Context Window**: Combines persona + memory + current situation
- **Dialogue Reply**: Generates natural, in-character responses
- **Action Intent**: Determines NPC behavior (help, betray, ignore, investigate)
- **Relationship Delta**: Updates trust level with the player
- **Memory Write**: Stores this interaction for future reference

## Features

### Core Features
✨ **Dynamic Personalities**: Each NPC has unique traits, beliefs, and motivations
🧠 **Memory System**: NPCs remember past interactions and reference them
😊 **Emotional States**: NPCs react emotionally and their mood affects responses
🎯 **Goal-Driven Behavior**: NPCs pursue their own objectives
🤝 **Relationship Tracking**: NPCs build trust or distrust based on interactions
🔒 **Secrets System**: NPCs have hidden information they won't reveal easily
🎭 **Natural Dialogue**: Powered by Groq's Llama 3.3 70B model

### Advanced Features ⭐ NEW
🗣️ **NPC-to-NPC Conversations**: Watch NPCs talk to each other with AI-generated dialogue
🌍 **Dynamic World Events**: Events happen that all NPCs react to (crimes, weather, supernatural)
💬 **Gossip Network**: Information spreads between NPCs organically
📊 **Visual Status Cards**: Beautiful terminal UI showing NPC states and relationships
👥 **Relationship Network**: NPCs form opinions about each other
📜 **Conversation History**: Full memory of all interactions with each NPC

### 🌍 Living World System ⭐⭐⭐ NEWEST
🤖 **Autonomous NPCs**: NPCs act independently with their own schedules and goals
🎯 **Dynamic Needs**: NPCs get hungry, tired, and seek social interaction
📋 **Multi-Step Planning**: NPCs create complex plans to achieve their goals
🏃 **Location & Movement**: NPCs move between locations pursuing objectives
💰 **Living Economy**: Dynamic prices based on supply and demand
⏰ **Time Simulation**: Day/night cycles affect NPC behavior
🌦️ **Weather System**: Dynamic weather that impacts the world
🔄 **Emergent Storytelling**: NPCs' autonomous actions create unique stories

➡️ **[See the Living World Guide](LIVING_WORLD_GUIDE.md)** for full details!

### 🤖 LangGraph Multi-Agent System ⭐⭐⭐⭐ CUTTING EDGE
🧠 **Structured Reasoning**: Perceive → Reason → Plan → Act → Reflect workflow
🔍 **Transparent Decisions**: Full reasoning traces for debugging
🤝 **Multi-Agent Coordination**: NPCs work together and negotiate
💬 **Message Passing**: Inter-agent communication infrastructure
🎯 **Conditional Logic**: Agents adapt based on state
📊 **Observable**: Inspect agent thoughts and internal monologue
🔄 **Scalable**: Production-ready multi-agent architecture

➡️ **[See the LangGraph Implementation Guide](LANGGRAPH_IMPLEMENTATION_SUMMARY.md)** for full details!

## Installation

1. **Clone the repository**
```bash
cd /path/to/MLFlow
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Get a Groq API key** (free)
   - Visit: https://console.groq.com/
   - Sign up and get your API key
   - Set it as an environment variable:
```bash
export GROQ_API_KEY='your-api-key-here'
```

## Quick Start

### 🚀 Run the LangGraph Multi-Agent Demo (NEWEST!)
```bash
pip install langgraph langchain-groq  # Install LangGraph first
python langgraph_demo.py              # Advanced agentic NPCs
```

### Run the Living World Demo
```bash
python quick_demo.py          # Quick feature demonstration
python living_world_demo.py   # Full interactive simulation
```

### Run the Interactive Game
```bash
python main.py
```

This launches an interactive terminal game where you can talk to pre-made NPCs:
- **Greta the Tavern Keeper**: Jovial, gossipy, knows everyone's business
- **Aldric the Scholar**: Brilliant but paranoid, researching forbidden magic
- **Captain Thorne**: Honorable guard captain, weary from years of service

### Run Examples
```bash
python example_usage.py
```

This demonstrates:
1. Simple conversations
2. Creating custom NPCs
3. Multi-NPC interactions
4. Emotion and memory systems

## Usage

### Creating a Custom NPC

```python
from npc_game.persona_core import PersonaCore
from npc_game.npc import NPC
from npc_game.llm_integration import GroqLLMClient
import os

# Define the persona
persona = PersonaCore(
    name="Thorin Ironforge",
    occupation="Master Blacksmith",
    traits=["gruff", "perfectionist", "kind-hearted"],
    backstory="A veteran blacksmith haunted by past mistakes.",
    core_motive="Create the perfect sword to honor his son's memory",
    beliefs=["Quality over quantity", "A craftsman's work is their legacy"],
    secrets=["He secretly helps poor families for free"]
)

# Create the NPC
npc = NPC(persona=persona)
npc.llm_client = GroqLLMClient(api_key=os.getenv('GROQ_API_KEY'))

# Interact
response = npc.interact("Hello, master blacksmith!")
print(response)
```

### Game Commands

When running the interactive game:
- `talk to <name>` - Select an NPC to talk to
- `status` - View current NPC's detailed status card
- `history` - View conversation history with current NPC
- `list` - List all available NPCs
- `overhear <npc1> <npc2>` - Watch two NPCs have a conversation
- `event` - Trigger a random world event
- `gossip` - See what gossip is spreading in the network
- `world` - View current world status
- `network` - View NPC relationship network
- `quit` - Exit the game

## Project Structure

```
npc_game/
├── __init__.py              # Package initialization
├── config.py                # Configuration settings
├── persona_core.py          # Persona/identity system
├── perception.py            # Perception and observation system
├── decision_engine.py       # Goals, emotions, and memory
├── llm_integration.py       # Groq API integration
├── npc.py                   # Main NPC class
└── game.py                  # Game loop and world management

main.py                      # Interactive game entry point
example_usage.py            # Usage examples
requirements.txt            # Python dependencies
README.md                   # This file
```

## How It Works

1. **Player Input**: You type what you want to say or do
2. **Perception**: NPC analyzes your words and tone
3. **Emotion Update**: NPC's emotional state changes based on your tone
4. **Context Building**: System combines:
   - NPC's personality and backstory
   - Current emotional state
   - Recent memories
   - Current goals
   - Relationship with you
5. **LLM Generation**: Groq API generates a response in-character
6. **Response Parsing**: Extracts dialogue, thoughts, and actions
7. **Memory Storage**: Stores this interaction for future recall
8. **Relationship Update**: Trust level changes based on interaction

## Customization

### Adding New Emotions
Edit `decision_engine.py` to add new `EmotionType` values.

### Adding New Tones
Edit `perception.py` to add new `Tone` values and detection logic.

### Changing LLM Model
Edit `llm_integration.py` to change the model (default: `llama-3.3-70b-versatile`).

### Adjusting Memory Limits
Edit `config.py` to change short/long-term memory limits.

## Future Enhancements

- 🗄️ Vector database integration for better long-term memory
- 🌍 Persistent world state across sessions
- 👥 NPC-to-NPC interactions
- 📊 Visual emotion/relationship graphs
- 🎨 GUI interface
- 🔊 Voice synthesis for NPC dialogue
- 🎲 D&D-style stat system integration

## License

MIT License - Feel free to use this for your projects!

## Credits

Architecture inspired by advanced NPC AI systems.  
Powered by Groq's ultra-fast LLM inference.

---

**Enjoy creating NPCs with soul!** 🎭✨
