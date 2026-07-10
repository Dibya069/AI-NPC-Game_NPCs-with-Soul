# Living World Simulation Architecture

## Vision
Transform the NPC system from a chatbot into a **living, breathing world** where NPCs have independent lives, plans, and interactions that continue even without player involvement.

## Core Philosophy
**The player is just one participant in an evolving world.**

---

## Architecture Overview

```
Game World (Root)
│
├── ⏰ Time Engine          - Manages world time, day/night cycles
├── 💰 Economy Engine       - Supply, demand, prices, trade
├── 🌦️  Weather Engine       - Dynamic weather affecting NPCs
├── 🎯 Event Engine         - Triggers world events
├── 🔍 Crime System         - Tracks illegal activities
├── 📜 Quest System         - Dynamic quest generation
├── ⭐ Reputation System    - Faction/town reputation
├── 💬 Gossip System        - Information spreads between NPCs
├── 🧠 Memory System        - World-wide memory storage
├── 🤝 Relationship Graph   - NPC-to-NPC relationships
├── 🗺️  Navigation System    - Locations and pathfinding
├── 📅 Scheduler            - NPC daily schedules
├── 🎯 AI Planner           - Multi-step NPC plans
└── 👥 NPC Manager          - All NPCs in the world
```

---

## Enhanced NPC Structure

```
NPC (Enhanced)
│
├── 🎭 Personality         - Existing persona core
├── 💎 Core Values         - What matters most
├── 🎯 Needs               - Hunger, sleep, safety, social
├── 📋 Goals               - Short & long-term goals
├── 🧠 Planner             - Creates multi-step plans
├── 😊 Emotions            - Current emotional state
├── 🧿 Beliefs             - What they think is true
├── 💭 Memories            - Personal history
├── 🤝 Relationships       - Bonds with other NPCs
├── 🎒 Inventory           - What they carry
├── 🛠️  Skills              - What they can do
├── 📅 Schedule            - Daily routine
├── 🧠 Knowledge           - What they know
├── 🏃 Current Action      - What they're doing now
├── 📍 Location            - Where they are
└── 🤖 LLM Brain           - AI decision making
```

---

## Key Features to Implement

### 1. **Autonomous NPC Behavior**
- NPCs pursue goals independently
- Multi-step plans (investigate → ask Greta → Greta tells Scholar → etc.)
- React to world state changes

### 2. **Dynamic Needs System**
```python
Needs {
    hunger: 0-100       # Gets hungry over time
    energy: 0-100       # Gets tired, needs sleep
    social: 0-100       # Wants to talk to others
    safety: 0-100       # Avoids danger
    wealth: 0-100       # Wants money/resources
}
```

### 3. **NPC-to-NPC Interactions**
- NPCs talk to each other without player
- Share information (gossip system)
- Form alliances/rivalries
- Plan together

### 4. **Location & Movement**
- NPCs move between locations
- Have schedules (morning: market, afternoon: tavern)
- Path finding

### 5. **Living Economy**
- Prices change based on supply/demand
- NPCs buy/sell goods
- Economic events affect behavior

### 6. **Multi-Step Planning**
```python
Plan: "Find the thief"
1. Ask town guard (Captain)
2. Investigate market
3. Question witnesses
4. Set trap
5. Capture thief
```

---

## Implementation Priority

### Phase 1: Foundation (Core Systems)
1. ✅ Enhanced NPC class with needs
2. ✅ Time engine
3. ✅ Location system
4. ✅ NPC scheduler

### Phase 2: Autonomy
1. ✅ Need-driven behavior
2. ✅ Multi-step planner
3. ✅ NPC-to-NPC dialogue
4. ✅ Autonomous actions

### Phase 3: World Dynamics
1. ✅ Gossip/information spread
2. ✅ Dynamic economy
3. ✅ Relationship evolution
4. ✅ Quest generation

### Phase 4: Advanced AI
1. ✅ Coalition forming
2. ✅ Emergent behavior
3. ✅ Long-term memory
4. ✅ Complex planning

---

## Example Simulation Loop

```
Every tick (e.g., 1 minute game time):

1. TIME ENGINE: Advance time
2. WEATHER: Update weather
3. ECONOMY: Update prices
4. NPCs: Update needs (hunger++, energy--)
5. NPCs: Evaluate current goals
6. NPCs: Plan actions based on needs/goals
7. NPCs: Execute actions
   - Move to location
   - Talk to other NPC
   - Buy/sell items
   - Work at job
8. GOSSIP: Information spreads
9. RELATIONSHIPS: Update based on interactions
10. EVENTS: Chance to trigger world event
11. PLAYER: Can act at any time
```

---

## Success Metrics

✅ NPCs have independent lives  
✅ World evolves without player  
✅ NPCs collaborate/conspire  
✅ Emergent storytelling  
✅ Player feels like part of living world  
