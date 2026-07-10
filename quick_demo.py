"""
Quick Living World Demo
Shows the new features in action
"""

from npc_game.enhanced_npc import EnhancedNPC
from npc_game.persona_core import PersonaCore
from npc_game.living_world import LivingWorld
from npc_game.needs_system import NeedType
from npc_game.planner import Plan, PlanStep, ActionType
from npc_game.gossip_system import Information, InformationType


def main():
    print("🌍 LIVING WORLD - QUICK DEMO")
    print("=" * 70)
    print()
    
    # Create world
    world = LivingWorld()
    
    # Create NPCs with interesting starting conditions
    greta = EnhancedNPC(
        persona=PersonaCore(
            name="Greta",
            occupation="Tavern Keeper",
            traits=["friendly", "gossipy"],
            backstory="Runs the tavern",
            core_motive="Keep customers happy"
        ),
        current_location="tavern"
    )
    
    # Make Greta hungry so she'll do something!
    greta.needs.needs[NeedType.HUNGER].value = 15  # Very hungry!
    
    marcus = EnhancedNPC(
        persona=PersonaCore(
            name="Marcus",
            occupation="Guard Captain",
            traits=["stern", "vigilant"],
            backstory="Protects the town",
            core_motive="Catch criminals"
        ),
        current_location="guard_house"
    )
    
    # Give Marcus a plan to investigate a crime
    marcus.planner.add_plan(Plan(
        goal="Investigate the theft",
        priority=9,
        steps=[
            PlanStep(ActionType.MOVE, "market", "Go to the crime scene"),
            PlanStep(ActionType.INVESTIGATE, "market", "Search for clues"),
            PlanStep(ActionType.MOVE, "tavern", "Question witnesses"),
            PlanStep(ActionType.TALK, "Greta", "Ask Greta what she knows"),
        ]
    ))
    
    world.add_npc(greta)
    world.add_npc(marcus)
    
    # Add some gossip
    world.gossip.create_news(
        "Someone stole from the market last night!",
        source="townspeople",
        importance=8
    )
    world.gossip.npc_learns_info("Marcus", 0)
    world.gossip.npc_learns_info("Greta", 0)
    
    print("\n📊 INITIAL STATE:")
    print("-" * 70)
    print(f"\n{greta.persona.name}:")
    print(f"  Location: {greta.current_location}")
    print(f"  Hunger: {int(greta.needs.needs[NeedType.HUNGER].value)}% (CRITICAL!)")
    print(f"  Energy: {int(greta.needs.needs[NeedType.ENERGY].value)}%")
    print(f"  Gold: {greta.inventory.gold}")
    
    print(f"\n{marcus.persona.name}:")
    print(f"  Location: {marcus.current_location}")
    print(f"  Current Plan: {marcus.planner.get_current_plan().goal}")
    print(f"  Steps: {len(marcus.planner.get_current_plan().steps)}")
    
    print("\n💬 Gossip:")
    print(f"  {world.gossip.information_pool[0].content}")
    
    print("\n" + "=" * 70)
    print("⏩ RUNNING SIMULATION (10 ticks)")
    print("=" * 70)
    
    # Run simulation
    for tick in range(10):
        print(f"\n🕐 TICK {tick + 1}")
        print("-" * 70)
        
        events = world.simulate_tick()
        
        # Show NPC actions
        for npc_action in events.get("npcs", []):
            print(f"  {npc_action}")
        
        # Show gossip sharing
        for gossip_event in events.get("gossip", []):
            print(f"  {gossip_event}")
        
        # Show world events
        for world_event in events.get("events", []):
            print(f"  {world_event}")
    
    print("\n" + "=" * 70)
    print("📊 FINAL STATE:")
    print("-" * 70)
    
    print(f"\n{greta.persona.name}:")
    print(f"  Location: {greta.current_location}")
    print(f"  Hunger: {int(greta.needs.needs[NeedType.HUNGER].value)}%")
    print(f"  Gold: {greta.inventory.gold}")
    if greta.inventory.items:
        print(f"  Items: {list(greta.inventory.items.keys())}")
    
    current_plan_greta = greta.planner.get_current_plan()
    if current_plan_greta:
        print(f"  Plan: {current_plan_greta.goal} - {current_plan_greta.get_progress()}")
    
    print(f"\n{marcus.persona.name}:")
    print(f"  Location: {marcus.current_location}")
    
    current_plan_marcus = marcus.planner.get_current_plan()
    if current_plan_marcus:
        print(f"  Plan: {current_plan_marcus.goal} - {current_plan_marcus.get_progress()}")
    else:
        print(f"  Plan: Completed investigation!")
    
    print("\n" + "=" * 70)
    print("✨ KEY FEATURES DEMONSTRATED:")
    print("=" * 70)
    print("✓ NPCs have dynamic needs (hunger, energy, etc.)")
    print("✓ NPCs create plans to satisfy needs")
    print("✓ NPCs follow multi-step plans autonomously")
    print("✓ NPCs move between locations")
    print("✓ World time advances")
    print("✓ Weather changes")
    print("✓ Information spreads through gossip system")
    print("✓ NPCs can share information when at same location")
    print("✓ Economy with dynamic prices")
    print("✓ NPCs can buy items")
    print("\n🎯 THIS IS JUST THE BEGINNING!")
    print("The world now has the foundation for:")
    print("  - NPC-to-NPC conversations")
    print("  - Coalition forming (NPCs planning together)")
    print("  - Crime and justice systems")
    print("  - Dynamic quests")
    print("  - Emergent storytelling")
    print("\n👉 Next: Enhance with LLM-driven NPC-to-NPC dialogue!")
    print("=" * 70)


if __name__ == "__main__":
    main()
