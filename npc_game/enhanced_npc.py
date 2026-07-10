"""
Enhanced NPC - Living NPC with needs, plans, and autonomous behavior
"""

from dataclasses import dataclass, field
from typing import Optional, Dict
from .npc import NPC
from .needs_system import NeedsSystem, NeedType
from .planner import Planner, Plan, ActionType, PlanStep
from .economy import Inventory


@dataclass
class EnhancedNPC(NPC):
    """
    Enhanced NPC with autonomous behavior, needs, planning, and inventory
    Extends the base NPC class with living world features
    """
    
    # New living world components
    needs: NeedsSystem = field(default_factory=NeedsSystem)
    planner: Planner = field(default_factory=Planner)
    inventory: Inventory = field(default_factory=Inventory)
    
    # Location and movement
    current_location: str = "tavern"
    home_location: str = "home"
    work_location: str = "market"
    
    # Relationships with other NPCs (NPC name -> trust level)
    npc_relationships: Dict[str, int] = field(default_factory=dict)
    
    # Knowledge about other NPCs locations
    known_locations: Dict[str, str] = field(default_factory=dict)
    
    # Current activity
    current_action: Optional[str] = None
    action_duration: int = 0  # Ticks remaining for current action
    
    def __post_init__(self):
        """Initialize enhanced NPC"""
        super().__post_init__()
        
        # Set reasonable starting gold based on occupation
        occupation_wealth = {
            "merchant": 200.0,
            "guard": 100.0,
            "scholar": 80.0,
            "innkeeper": 150.0,
            "farmer": 60.0,
            "noble": 500.0,
        }
        
        for occupation, wealth in occupation_wealth.items():
            if occupation.lower() in self.persona.occupation.lower():
                self.inventory.gold = wealth
                break
    
    def autonomous_tick(self) -> str:
        """
        Called each game tick - NPC acts autonomously
        Returns description of what NPC did
        """
        actions_taken = []
        
        # 1. Update needs (they degrade over time)
        self.needs.update_all()
        
        # 2. Handle ongoing action
        if self.action_duration > 0:
            self.action_duration -= 1
            if self.action_duration == 0:
                actions_taken.append(self._complete_current_action())
        
        # 3. Check if needs are critical - create urgent plans
        critical_needs = self.needs.get_critical_needs()
        if critical_needs and not self.planner.get_current_plan():
            # Create plan to satisfy most urgent need
            urgent_need = self.needs.get_most_urgent_need()
            if urgent_need:
                plan = self.planner.create_need_satisfaction_plan(
                    urgent_need.value, 
                    self.current_location
                )
                self.planner.add_plan(plan)
                actions_taken.append(f"💭 Plans to {plan.goal}")
        
        # 4. Execute current plan step
        if self.action_duration == 0:  # Only if not busy
            current_step = self.planner.execute_current_step()
            if current_step:
                result = self._execute_plan_step(current_step)
                actions_taken.append(result)
        
        # 5. Emotion decay
        self.decision_engine.emotion_state.decay_emotion(0.05)
        
        return " | ".join(actions_taken) if actions_taken else f"🧍 {self.persona.name} idles at {self.current_location}"
    
    def _execute_plan_step(self, step: PlanStep) -> str:
        """Execute a single plan step"""
        if step.action == ActionType.MOVE:
            return self._action_move(step.target)
        
        elif step.action == ActionType.EAT:
            return self._action_eat()
        
        elif step.action == ActionType.REST:
            return self._action_rest()
        
        elif step.action == ActionType.WORK:
            return self._action_work()
        
        elif step.action == ActionType.TALK:
            # This would need another NPC to talk to
            return self._action_socialize()
        
        elif step.action == ActionType.BUY:
            return self._action_buy(step.target)
        
        elif step.action == ActionType.WAIT:
            return f"⏸️  {self.persona.name} waits"
        
        else:
            return f"❓ {self.persona.name} attempts to {step.action.value}"
    
    def _action_move(self, destination: str) -> str:
        """Move to a location"""
        if destination:
            old_location = self.current_location
            self.current_location = destination
            self.planner.complete_current_step()
            return f"🚶 {self.persona.name} moves from {old_location} to {destination}"
        return f"❌ {self.persona.name} doesn't know where to go"
    
    def _action_eat(self) -> str:
        """Eat food"""
        if self.inventory.has_item("food"):
            self.inventory.remove_item("food")
            self.needs.satisfy_need(NeedType.HUNGER, 50)
            self.planner.complete_current_step()
            return f"🍖 {self.persona.name} eats food (+50 hunger)"
        return f"❌ {self.persona.name} has no food!"
    
    def _action_rest(self) -> str:
        """Rest/sleep"""
        self.current_action = "sleeping"
        self.action_duration = 4  # Sleep for 4 ticks (1 hour)
        return f"😴 {self.persona.name} goes to sleep"
    
    def _action_work(self) -> str:
        """Work at job"""
        self.current_action = "working"
        self.action_duration = 8  # Work for 8 ticks (2 hours)
        return f"🔨 {self.persona.name} starts working"
    
    def _action_socialize(self) -> str:
        """Socialize (satisfy social need)"""
        self.needs.satisfy_need(NeedType.SOCIAL, 30)
        self.planner.complete_current_step()
        return f"💬 {self.persona.name} chats with others (+30 social)"
    
    def _action_buy(self, item_name: str) -> str:
        """Buy an item (requires economy system integration)"""
        # For now, simulate buying
        cost = 5.0 if item_name == "food" else 10.0
        if self.inventory.gold >= cost:
            self.inventory.gold -= cost
            self.inventory.add_item(item_name or "food")
            self.planner.complete_current_step()
            return f"💰 {self.persona.name} buys {item_name} for {cost} gold"
        return f"❌ {self.persona.name} can't afford {item_name}"
    
    def _complete_current_action(self) -> str:
        """Complete ongoing action"""
        action = self.current_action
        self.current_action = None
        
        if action == "sleeping":
            self.needs.satisfy_need(NeedType.ENERGY, 80)
            self.planner.complete_current_step()
            return f"😊 {self.persona.name} wakes up refreshed (+80 energy)"
        
        elif action == "working":
            earned = 20.0
            self.inventory.gold += earned
            self.needs.satisfy_need(NeedType.WEALTH, 30)
            self.planner.complete_current_step()
            return f"💼 {self.persona.name} finishes work (earned {earned} gold)"
        
        return f"✓ {self.persona.name} finishes {action}"
