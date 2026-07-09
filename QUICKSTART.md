# Quick Start Guide 🚀

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install groq
```

### 2. Get Your FREE Groq API Key
1. Visit: https://console.groq.com/
2. Sign up (it's free!)
3. Create an API key
4. Copy the key

### 3. Set Environment Variable

**MacOS/Linux:**
```bash
export GROQ_API_KEY='your-api-key-here'
```

**Windows (CMD):**
```cmd
set GROQ_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your-api-key-here"
```

## Run the Game

### Option 1: Interactive Game
```bash
python main.py
```

This starts an interactive terminal game where you can:
- Talk to 3 pre-made NPCs with unique personalities
- See their emotional states change
- Build relationships through conversation
- Discover their secrets (if they trust you!)

**Example Session:**
```
[You] talk to Greta
[You approach Greta the Tavern Keeper]
[Greta]: Hello there.

[You -> Greta] What's the best drink you have?
[Greta]: Ah, if you've got the coin, our Golden Mead is legendary! 
         But between you and me, the regular ale is just as good...

[You -> Greta] status
--- Greta the Tavern Keeper ---
Emotion: happy
Trust level: 5/100
Current goal: Wants to keep her tavern profitable and be the center of town gossip
```

### Option 2: Run Examples
```bash
python example_usage.py
```

This runs 4 demonstration scripts showing:
1. **Simple Conversation** - Basic NPC interaction
2. **Custom NPC Creation** - How to make your own NPCs
3. **Multi-NPC Game** - Talking to different NPCs
4. **Emotions & Memory** - How NPCs remember and react

## Create Your First Custom NPC

```python
from npc_game.persona_core import PersonaCore
from npc_game.npc import NPC
from npc_game.llm_integration import GroqLLMClient
import os

# 1. Define who they are
my_npc = PersonaCore(
    name="Elara the Herbalist",
    occupation="Healer",
    traits=["wise", "mysterious", "cautious"],
    backstory="Elara studied forbidden healing magic in the Eastern Kingdoms.",
    core_motive="Wants to cure a plague that's spreading in secret",
    beliefs=["All life is sacred", "Knowledge should be shared"],
    secrets=["She's infected with the plague herself"]
)

# 2. Create the NPC
npc = NPC(persona=my_npc)
npc.llm_client = GroqLLMClient(api_key=os.getenv('GROQ_API_KEY'))

# 3. Interact!
response = npc.interact("Can you help me? I'm feeling sick.")
print(f"[Elara]: {response}")
```

## Understanding NPC Responses

NPCs generate responses considering:
- ✅ Their personality traits and beliefs
- ✅ Their current emotional state
- ✅ Past interactions with you (memory)
- ✅ Their relationship/trust level with you
- ✅ Their secrets (which they protect)
- ✅ Their goals and motivations

## Game Commands

| Command | Description |
|---------|-------------|
| `talk to <name>` | Start conversation with an NPC |
| `status` | View NPC's emotional state and trust |
| `list` | Show all available NPCs |
| `quit` | Exit the game |

## Tips for Better Interactions

1. **Be Consistent**: NPCs remember what you say!
2. **Watch Their Emotions**: An angry NPC won't help you
3. **Build Trust**: Friendly interactions increase trust
4. **Discover Secrets**: High trust NPCs reveal more
5. **Match Their Personality**: Aggressive NPCs respect strength, scholarly NPCs appreciate intelligence

## Pre-made NPCs

### Greta the Tavern Keeper
- **Personality**: Jovial, gossipy, greedy
- **Likes**: Money, gossip, regular customers
- **Secrets**: Waters down wine, knows about smuggling

### Aldric the Scholar
- **Personality**: Brilliant, paranoid, obsessive
- **Likes**: Knowledge, research, being proven right
- **Secrets**: Summoned something dangerous, stole forbidden books

### Captain Thorne
- **Personality**: Honorable, stern, duty-bound
- **Likes**: Justice, order, respect for the law
- **Secrets**: Overwhelmed and thinking of retiring

## Troubleshooting

**"GROQ_API_KEY not found"**
- Make sure you've set the environment variable
- Restart your terminal after setting it

**"ModuleNotFoundError: No module named 'groq'"**
- Run: `pip install groq`

**NPCs give generic responses**
- Your API key might not be set correctly
- Check the key is valid at https://console.groq.com/

## Next Steps

- Read `README.md` for detailed documentation
- Check `example_usage.py` for more code examples
- Create your own NPCs with unique personalities
- Experiment with different interaction styles

**Have fun creating NPCs with soul!** 🎭✨
