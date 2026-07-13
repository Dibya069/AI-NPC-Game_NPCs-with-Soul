"""
Multi-Agent System Orchestrator
Manages multiple LangGraph agents and their interactions
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field

from .langgraph_agent import NPCAgent
from .agent_state import Message, WorldState
from .enhanced_npc import EnhancedNPC
from .living_world import LivingWorld


@dataclass
class MultiAgentSystem:
    """
    Orchestrates multiple NPC agents
    Handles message passing, conflict resolution, and coordination
    """
    
    agents: Dict[str, NPCAgent] = field(default_factory=dict)
    world: Optional[LivingWorld] = None
    api_key: Optional[str] = None
    
    # Message queue
    message_queue: List[Message] = field(default_factory=list)
    
    # Execution order
    agent_order: List[str] = field(default_factory=list)
    current_tick: int = 0
    
    def add_agent(self, enhanced_npc: EnhancedNPC) -> NPCAgent:
        """Add a new agent to the system"""
        agent = NPCAgent(enhanced_npc, api_key=self.api_key)
        self.agents[enhanced_npc.persona.name] = agent
        self.agent_order.append(enhanced_npc.persona.name)
        
        print(f"✓ Added LangGraph agent: {enhanced_npc.persona.name}")
        return agent
    
    def step_all_agents(self, world_state: Optional[WorldState] = None):
        """Execute one step for all agents"""
        
        results = {}
        
        # Each agent takes a turn
        for agent_name in self.agent_order:
            agent = self.agents[agent_name]
            
            # Prepare world state for this agent
            agent_world_state = self._prepare_world_state(agent_name, world_state)
            
            # Agent takes a step
            result = agent.step(agent_world_state)
            results[agent_name] = result
        
        # Process message queue
        self._process_messages()
        
        # Update world if available
        if self.world:
            self.world.simulate_tick()
        
        self.current_tick += 1
        
        return results
    
    def _prepare_world_state(self, agent_name: str, base_world_state: Optional[WorldState]) -> dict:
        """Prepare world state specific to an agent"""
        
        agent = self.agents[agent_name]
        location = agent.npc.current_location
        
        # Find nearby NPCs at same location
        nearby_npcs = [
            name for name, other_agent in self.agents.items()
            if name != agent_name and other_agent.npc.current_location == location
        ]
        
        world_state = base_world_state or {}
        world_state["nearby_npcs"] = nearby_npcs
        world_state["tick"] = self.current_tick
        
        return world_state
    
    def _process_messages(self):
        """Deliver messages between agents"""
        
        for agent in self.agents.values():
            # Get messages from outbox
            for msg in agent.state.get("messages_outbox", []):
                self.message_queue.append(msg)
            
            # Clear outbox
            agent.state["messages_outbox"] = []
        
        # Deliver messages
        for msg in self.message_queue:
            if msg.to_agent in self.agents:
                self.agents[msg.to_agent].receive_message(msg)
        
        # Clear queue
        self.message_queue = []
    
    def agent_send_message(self, from_agent: str, to_agent: str, 
                          message_type: str, content: str):
        """Helper: One agent sends message to another"""
        if from_agent in self.agents:
            self.agents[from_agent].send_message(to_agent, message_type, content)
    
    def get_agent_thoughts(self, agent_name: str) -> dict:
        """Get an agent's internal state for debugging"""
        if agent_name not in self.agents:
            return {}
        
        agent = self.agents[agent_name]
        return {
            "name": agent_name,
            "location": agent.state["location"],
            "status": agent.state["current_status"],
            "goal": agent.state.get("current_goal"),
            "plan": agent.state.get("current_plan"),
            "reasoning": agent.get_reasoning_trace()[-5:],  # Last 5 thoughts
            "monologue": agent.get_internal_monologue()[-3:]  # Last 3 thoughts
        }
    
    def get_all_agent_thoughts(self) -> dict:
        """Get thoughts from all agents"""
        return {
            name: self.get_agent_thoughts(name)
            for name in self.agents.keys()
        }
    
    def visualize_agent_states(self) -> str:
        """Create a visual summary of all agents"""
        lines = ["=" * 70, "🤖 MULTI-AGENT SYSTEM STATE", "=" * 70, ""]
        
        for agent_name, agent in self.agents.items():
            state = agent.state
            
            lines.append(f"👤 {agent_name}")
            lines.append(f"   📍 Location: {state['location']}")
            lines.append(f"   🎯 Status: {state['current_status']}")
            
            if state.get("current_goal"):
                lines.append(f"   🎯 Goal: {state['current_goal']}")
            
            if state.get("current_plan"):
                plan = state["current_plan"]
                step = state.get("plan_step", 0)
                total = len(plan.get("steps", []))
                lines.append(f"   📋 Plan: {plan['goal']} ({step}/{total} steps)")
            
            # Recent thoughts
            monologue = agent.get_internal_monologue()
            if monologue:
                lines.append(f"   💭 Thinking: \"{monologue[-1]}\"")
            
            # Messages
            inbox_count = len(state.get("messages_inbox", []))
            outbox_count = len(state.get("messages_outbox", []))
            if inbox_count or outbox_count:
                lines.append(f"   📧 Messages: {inbox_count} received, {outbox_count} to send")
            
            lines.append("")
        
        lines.append("=" * 70)
        return "\n".join(lines)
    
    def run_simulation(self, ticks: int = 10, verbose: bool = True):
        """Run the multi-agent simulation for N ticks"""
        
        for tick in range(ticks):
            if verbose:
                print(f"\n{'='*70}")
                print(f"🕐 TICK {self.current_tick + 1}")
                print('='*70)
            
            # Step all agents
            self.step_all_agents()
            
            if verbose:
                # Show what each agent did
                for agent_name, agent in self.agents.items():
                    last_action = agent.state.get("last_action", "idle")
                    print(f"  {agent_name}: {last_action}")
                
                # Show recent thoughts
                print("\n💭 Agent Thoughts:")
                for agent_name, agent in self.agents.items():
                    thoughts = agent.get_reasoning_trace()
                    if thoughts:
                        latest = thoughts[-1] if thoughts else "..."
                        print(f"  {agent_name}: {latest}")
