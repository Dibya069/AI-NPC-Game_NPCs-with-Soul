"""
Agent State Definitions for LangGraph
Defines the state schema for NPC agents
"""

from typing import TypedDict, List, Optional, Dict, Any, Annotated
from dataclasses import dataclass, field
from enum import Enum
import operator


class AgentStatus(Enum):
    """Current status of the agent"""
    IDLE = "idle"
    THINKING = "thinking"
    PLANNING = "planning"
    ACTING = "acting"
    COMMUNICATING = "communicating"
    WAITING = "waiting"


@dataclass
class Observation:
    """Something the agent perceives"""
    type: str  # "world_event", "npc_action", "player_action", "message"
    content: str
    source: str
    timestamp: int
    importance: int = 5  # 1-10


@dataclass
class Message:
    """Message between agents"""
    from_agent: str
    to_agent: str
    message_type: str  # "request", "inform", "propose", "accept", "reject"
    content: str
    priority: int = 5


@dataclass
class ActionResult:
    """Result of an action execution"""
    success: bool
    description: str
    effects: Dict[str, Any] = field(default_factory=dict)
    

class AgentState(TypedDict):
    """
    Complete state for a LangGraph NPC agent
    Uses Annotated types for proper state reduction
    """
    
    # ===== IDENTITY =====
    npc_name: str
    agent_id: str
    
    # ===== PERCEPTION =====
    observations: Annotated[List[Observation], operator.add]  # Append new observations
    world_state: Dict[str, Any]  # Current world state snapshot
    nearby_npcs: List[str]  # NPCs at same location
    
    # ===== COGNITION =====
    beliefs: Dict[str, Any]  # What the agent believes is true
    knowledge: Annotated[List[str], operator.add]  # Facts the agent knows
    current_goal: Optional[str]  # Primary goal
    goals: List[str]  # All active goals
    
    # ===== PLANNING =====
    current_plan: Optional[Dict[str, Any]]  # Active plan
    plan_step: int  # Current step in plan
    alternative_plans: List[Dict[str, Any]]  # Backup plans
    
    # ===== SOCIAL =====
    messages_inbox: Annotated[List[Message], operator.add]  # Received messages
    messages_outbox: List[Message]  # Messages to send
    active_conversations: List[str]  # Who we're talking to
    
    # ===== EXECUTION =====
    last_action: Optional[str]  # Last action taken
    action_result: Optional[ActionResult]  # Result of last action
    current_status: str  # Current agent status
    
    # ===== REASONING =====
    reasoning_trace: Annotated[List[str], operator.add]  # Thought process (for debugging)
    internal_monologue: Annotated[List[str], operator.add]  # What agent is "thinking"
    
    # ===== CONTROL FLOW =====
    should_replan: bool  # Flag to trigger replanning
    needs_help: bool  # Flag to request assistance
    next_node: Optional[str]  # For conditional routing
    iteration_count: int  # Prevent infinite loops
    
    # ===== CONTEXT =====
    tick: int  # Current world tick
    location: str  # Current location


@dataclass
class CoalitionState(TypedDict):
    """State for multi-agent coalition"""
    coalition_id: str
    members: List[str]  # Agent IDs
    leader: Optional[str]
    shared_goal: str
    shared_plan: Optional[Dict[str, Any]]
    member_roles: Dict[str, str]  # agent_id -> role
    communication_log: Annotated[List[Message], operator.add]
    status: str  # "forming", "active", "completed", "dissolved"


@dataclass
class WorldState(TypedDict):
    """Global world state accessible to all agents"""
    current_time: str
    current_tick: int
    weather: str
    locations: Dict[str, Any]
    economy: Dict[str, Any]
    recent_events: List[str]
    npc_locations: Dict[str, str]  # npc_name -> location
    

def create_initial_agent_state(npc_name: str, location: str = "town_square") -> AgentState:
    """Create initial state for a new agent"""
    return AgentState(
        # Identity
        npc_name=npc_name,
        agent_id=f"agent_{npc_name.lower()}",
        
        # Perception
        observations=[],
        world_state={},
        nearby_npcs=[],
        
        # Cognition
        beliefs={},
        knowledge=[],
        current_goal=None,
        goals=[],
        
        # Planning
        current_plan=None,
        plan_step=0,
        alternative_plans=[],
        
        # Social
        messages_inbox=[],
        messages_outbox=[],
        active_conversations=[],
        
        # Execution
        last_action=None,
        action_result=None,
        current_status=AgentStatus.IDLE.value,
        
        # Reasoning
        reasoning_trace=[],
        internal_monologue=[],
        
        # Control
        should_replan=False,
        needs_help=False,
        next_node=None,
        iteration_count=0,
        
        # Context
        tick=0,
        location=location
    )
