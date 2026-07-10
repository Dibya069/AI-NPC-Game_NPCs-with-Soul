"""
AI Planner System
NPCs create multi-step plans to achieve goals
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum


class ActionType(Enum):
    """Types of actions NPCs can take"""
    MOVE = "move"              # Move to location
    TALK = "talk"              # Talk to NPC
    WORK = "work"              # Work at job
    REST = "rest"              # Sleep/rest
    EAT = "eat"                # Eat food
    BUY = "buy"                # Purchase item
    SELL = "sell"              # Sell item
    INVESTIGATE = "investigate" # Investigate something
    WAIT = "wait"              # Wait/idle
    SEARCH = "search"          # Search for something
    GUARD = "guard"            # Guard location
    STEAL = "steal"            # Steal item (illegal)
    ATTACK = "attack"          # Attack NPC (illegal)


class PlanStatus(Enum):
    """Status of a plan"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class PlanStep:
    """A single step in a plan"""
    action: ActionType
    target: Optional[str] = None  # Location, NPC, or item name
    description: str = ""
    completed: bool = False
    
    def execute_description(self) -> str:
        """Get description of executing this step"""
        if self.action == ActionType.MOVE:
            return f"Moving to {self.target}"
        elif self.action == ActionType.TALK:
            return f"Talking to {self.target}"
        elif self.action == ActionType.INVESTIGATE:
            return f"Investigating {self.target}"
        else:
            return f"{self.action.value.capitalize()}: {self.description}"


@dataclass
class Plan:
    """A multi-step plan to achieve a goal"""
    goal: str
    steps: List[PlanStep] = field(default_factory=list)
    status: PlanStatus = PlanStatus.PENDING
    current_step: int = 0
    priority: int = 5  # 1-10, higher = more important
    
    def get_current_step(self) -> Optional[PlanStep]:
        """Get the current step to execute"""
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None
    
    def advance_step(self):
        """Mark current step complete and advance"""
        if self.current_step < len(self.steps):
            self.steps[self.current_step].completed = True
            self.current_step += 1
            
            if self.current_step >= len(self.steps):
                self.status = PlanStatus.COMPLETED
    
    def is_complete(self) -> bool:
        """Check if plan is complete"""
        return self.status == PlanStatus.COMPLETED
    
    def cancel(self):
        """Cancel this plan"""
        self.status = PlanStatus.CANCELLED
    
    def get_progress(self) -> str:
        """Get progress string"""
        total = len(self.steps)
        complete = sum(1 for step in self.steps if step.completed)
        return f"{complete}/{total} steps complete"


@dataclass
class Planner:
    """Creates and manages plans for an NPC"""
    
    active_plans: List[Plan] = field(default_factory=list)
    completed_plans: List[Plan] = field(default_factory=list)
    
    def add_plan(self, plan: Plan):
        """Add a new plan"""
        self.active_plans.append(plan)
        self.active_plans.sort(key=lambda p: p.priority, reverse=True)
    
    def get_current_plan(self) -> Optional[Plan]:
        """Get the highest priority active plan"""
        active = [p for p in self.active_plans 
                 if p.status in [PlanStatus.PENDING, PlanStatus.IN_PROGRESS]]
        
        if active:
            return active[0]
        return None
    
    def execute_current_step(self) -> Optional[PlanStep]:
        """Get current step to execute"""
        plan = self.get_current_plan()
        if plan:
            plan.status = PlanStatus.IN_PROGRESS
            return plan.get_current_step()
        return None
    
    def complete_current_step(self):
        """Mark current step as complete"""
        plan = self.get_current_plan()
        if plan:
            plan.advance_step()
            
            if plan.is_complete():
                self.active_plans.remove(plan)
                self.completed_plans.append(plan)
    
    def create_need_satisfaction_plan(self, need_type: str, npc_location: str) -> Plan:
        """Create a plan to satisfy a specific need"""
        from .needs_system import NeedType
        
        if need_type == NeedType.HUNGER.value:
            return Plan(
                goal=f"Satisfy hunger",
                priority=8,
                steps=[
                    PlanStep(ActionType.MOVE, "tavern", "Go to tavern"),
                    PlanStep(ActionType.BUY, "food", "Buy food"),
                    PlanStep(ActionType.EAT, "food", "Eat the food"),
                ]
            )
        
        elif need_type == NeedType.ENERGY.value:
            return Plan(
                goal=f"Rest and recover energy",
                priority=9,
                steps=[
                    PlanStep(ActionType.MOVE, "home", "Go home"),
                    PlanStep(ActionType.REST, None, "Sleep"),
                ]
            )
        
        elif need_type == NeedType.SOCIAL.value:
            return Plan(
                goal=f"Socialize",
                priority=5,
                steps=[
                    PlanStep(ActionType.MOVE, "tavern", "Go to tavern"),
                    PlanStep(ActionType.TALK, "anyone", "Chat with someone"),
                ]
            )
        
        elif need_type == NeedType.WEALTH.value:
            return Plan(
                goal=f"Earn money",
                priority=6,
                steps=[
                    PlanStep(ActionType.MOVE, "workplace", "Go to work"),
                    PlanStep(ActionType.WORK, None, "Work"),
                ]
            )
        
        # Default plan: wait
        return Plan(
            goal="Wait",
            priority=1,
            steps=[PlanStep(ActionType.WAIT, None, "Idle")]
        )
