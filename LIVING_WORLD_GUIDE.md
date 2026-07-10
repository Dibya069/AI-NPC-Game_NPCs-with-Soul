# Living World System Guide

## 🌍 Overview

The Living World system transforms NPCs from simple chatbots into **autonomous agents** living in a dynamic, evolving world. NPCs now have needs, make plans, move around, interact with each other, and pursue goals independently of the player.

## ✨ What's New

### Before (Simple Chat):
```
Player → NPC → Response
```

### Now (Living World):
```
World Simulation Loop (Every Tick):
├── Time advances
├── Weather changes  
├── NPCs update needs
├── NPCs make plans
├── NPCs execute actions
├── NPCs move locations
├── NPCs share gossip
├── Economy fluctuates
└── Random events occur
```

---

## 🧩 Architecture

```
LivingWorld
│
├── WorldSimulation      ⏰ Time, weather, locations
├── GossipSystem         💬 Information spreading
├── Economy              💰 Dynamic prices, trading
├── EventSystem          🎯 Random world events
└── NPCs                 👥 Enhanced autonomous NPCs
    │
    ├── Persona          🎭 Identity (existing)
    ├── Needs            🎯 Hunger, energy, social, wealth
    ├── Planner          📋 Multi-step plans
    ├── Inventory        🎒 Items and gold
    ├── Location         📍 Current position
    └── Relationships    🤝 Bonds with other NPCs
```

---

## 🎯 Key Systems

### 1. Needs System

NPCs have dynamic needs that drive behavior:

| Need       | Description                    | Decay Rate |
|------------|--------------------------------|------------|
| 🍖 Hunger  | Gets hungry over time          | Fast       |
| ⚡ Energy  | Gets tired, needs sleep        | Medium     |
| 👥 Social  | Wants to interact with others  | Slow       |
| 🛡️ Safety  | Avoids danger                  | Very slow  |
| 💰 Wealth  | Wants money/resources          | Slow       |
| 🔍 Curiosity | Wants to explore/learn       | Medium     |

**Example:**
```python
# NPC automatically creates plans when needs are urgent
npc.needs.needs[NeedType.HUNGER].value = 15  # Critical!
npc.autonomous_tick()  
# → NPC creates plan: Go to tavern → Buy food → Eat
```

### 2. Planning System

NPCs create multi-step plans to achieve goals:

```python
Plan: "Investigate theft"
├── Step 1: Move to market
├── Step 2: Search for clues  
├── Step 3: Move to tavern
└── Step 4: Question Greta
```

**Actions Available:**
- MOVE - Travel to location
- TALK - Converse with NPC
- WORK - Earn money
- REST - Recover energy
- EAT - Satisfy hunger
- BUY/SELL - Trade items
- INVESTIGATE - Search for info
- GUARD - Protect location

### 3. Gossip System

Information spreads organically between NPCs:

```python
# Information gets created
gossip.create_news("Thief seen near market", source="Guard", importance=8)

# NPCs learn it
gossip.npc_learns_info("Greta", info_id)

# NPCs share when they meet
shared = gossip.npcs_share_information("Greta", "Marcus")
# → Marcus now knows about the thief!
```

### 4. Dynamic Economy

Prices change based on supply and demand:

```python
# Someone buys food
economy.buy_item("food", quantity=5)
# → Supply decreases → Price increases!

# World event: "Poor harvest" 
economy.apply_event_effect("Poor crop harvest")
# → Food supply drops → Prices surge!
```

### 5. World Simulation

Time, weather, and locations:

```python
world = WorldSimulation()

# Each tick
events = world.tick()
# → Time: Day 1, 9:00 AM
# → Weather: ☀️ Clear skies
# → NPCs at locations tracked
```

---

## 🚀 Quick Start

### Basic Usage

```python
from npc_game.living_world import LivingWorld
from npc_game.enhanced_npc import EnhancedNPC
from npc_game.persona_core import PersonaCore

# Create world
world = LivingWorld()

# Create NPC
npc = EnhancedNPC(
    persona=PersonaCore(
        name="Greta",
        occupation="Tavern Keeper",
        traits=["friendly", "gossipy"]
    )
)

world.add_npc(npc)

# Run simulation
world.run_simulation(ticks=10)
```

### Run the Demo

```bash
python quick_demo.py       # Quick feature demonstration
python living_world_demo.py  # Full interactive simulation
```

---

## 📖 Examples

### Example 1: NPC Collaborates

```python
# Marcus needs to find a thief
# Creates plan: Ask Greta → Greta tells Scholar → Scholar warns thief
marcus.planner.add_plan(Plan(
    goal="Find the thief",
    steps=[
        PlanStep(ActionType.MOVE, "tavern"),
        PlanStep(ActionType.TALK, "Greta"),
        # Greta shares info...
    ]
))
```

### Example 2: Need-Driven Behavior

```python
# Greta gets hungry
greta.needs.needs[NeedType.HUNGER].value = 10  # Critical!

# Next tick, she automatically:
# 1. Creates plan to satisfy hunger
# 2. Moves to tavern  
# 3. Buys food
# 4. Eats and recovers
```

### Example 3: Information Spreads

```python
# Crime occurs
world.gossip.create_news("Market robbed!", source="witness", importance=9)

# Guard learns about it
world.gossip.npc_learns_info("Captain Marcus", 0)

# Later, Marcus talks to Greta at tavern
# → Information automatically shared!
```

---

## 🔮 Future Enhancements

### Phase 1: ✅ Complete
- ✅ Needs system
- ✅ Multi-step planner
- ✅ Autonomous movement
- ✅ Gossip network
- ✅ Dynamic economy

### Phase 2: 🚧 Next
- 🚧 LLM-driven NPC-to-NPC dialogue
- 🚧 Coalition forming (NPCs planning together)
- 🚧 Crime and justice system
- 🚧 Dynamic quest generation

### Phase 3: 🔮 Future
- Advanced AI emergent behavior
- Complex relationship dynamics
- Faction systems
- Long-term world memory

---

## 🎮 Design Philosophy

> **The player is just one participant in an evolving world.**

NPCs should:
1. Have independent lives and routines
2. Pursue goals without player involvement
3. Form relationships with each other
4. React to world changes dynamically
5. Create emergent stories through interactions

---

## 📚 API Reference

See individual files:
- `needs_system.py` - Needs and motivation
- `planner.py` - Multi-step planning
- `gossip_system.py` - Information spreading
- `economy.py` - Dynamic economy
- `world_simulation.py` - Time, weather, locations
- `enhanced_npc.py` - Autonomous NPC behavior
- `living_world.py` - Main orchestrator

---

**Built with ❤️ for creating living, breathing worlds**
