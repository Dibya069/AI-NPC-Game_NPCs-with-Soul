"""
LangGraph NPC Agent
Advanced autonomous agent using LangGraph for decision-making
"""

from typing import Literal, Optional
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from .agent_state import AgentState, Observation, Message, ActionResult, create_initial_agent_state
from .enhanced_npc import EnhancedNPC
from .needs_system import NeedType


class NPCAgent:
    """
    LangGraph-powered NPC agent with advanced reasoning
    """
    
    def __init__(self, enhanced_npc: EnhancedNPC, api_key: Optional[str] = None):
        """Initialize the agent"""
        self.npc = enhanced_npc
        self.state = create_initial_agent_state(
            npc_name=enhanced_npc.persona.name,
            location=enhanced_npc.current_location
        )
        
        # LLM for reasoning
        self.llm = None
        if api_key:
            self.llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                api_key=api_key
            )
        
        # Build the agent graph
        self.graph = self._build_graph()
        self.app = self.graph.compile()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("perceive", self.perceive_node)
        workflow.add_node("reason", self.reason_node)
        workflow.add_node("plan", self.plan_node)
        workflow.add_node("decide", self.decide_node)
        workflow.add_node("act", self.act_node)
        workflow.add_node("reflect", self.reflect_node)
        workflow.add_node("communicate", self.communicate_node)
        
        # Set entry point
        workflow.set_entry_point("perceive")
        
        # Add edges
        workflow.add_edge("perceive", "reason")
        workflow.add_edge("reason", "decide")
        
        # Conditional edge from decide
        workflow.add_conditional_edges(
            "decide",
            self.route_after_decision,
            {
                "plan": "plan",
                "act": "act",
                "communicate": "communicate",
                "end": END
            }
        )
        
        workflow.add_edge("plan", "act")
        workflow.add_edge("communicate", "act")
        workflow.add_edge("act", "reflect")
        workflow.add_edge("reflect", END)
        
        return workflow
    
    # ===== NODES =====
    
    def perceive_node(self, state: AgentState) -> AgentState:
        """Perceive the world and update observations"""
        state["reasoning_trace"].append(f"[PERCEIVE] {self.npc.persona.name} observes surroundings")
        
        # Update world state from NPC
        state["world_state"] = {
            "location": self.npc.current_location,
            "tick": state["tick"],
            "nearby_npcs": state.get("nearby_npcs", [])
        }
        
        # Check needs and create observations
        urgent_need = self.npc.needs.get_most_urgent_need()
        if urgent_need:
            need_value = self.npc.needs.needs[urgent_need].value
            obs = Observation(
                type="internal_state",
                content=f"I feel {urgent_need.value} ({int(need_value)}%)",
                source="self",
                timestamp=state["tick"],
                importance=8 if need_value < 30 else 5
            )
            state["observations"].append(obs)
            state["reasoning_trace"].append(f"  → Feeling {urgent_need.value} (urgent!)")
        
        return state
    
    def reason_node(self, state: AgentState) -> AgentState:
        """Analyze situation and update beliefs"""
        state["reasoning_trace"].append(f"[REASON] Analyzing situation...")
        state["current_status"] = "thinking"
        
        # Simple rule-based reasoning for now
        # TODO: Use LLM for complex reasoning
        
        # Check if current plan is still valid
        if state["current_plan"] and state["plan_step"] >= len(state["current_plan"].get("steps", [])):
            state["current_plan"] = None
            state["reasoning_trace"].append("  → Current plan completed")
        
        # Check for urgent needs
        urgent_need = self.npc.needs.get_most_urgent_need()
        if urgent_need and not state["current_plan"]:
            state["current_goal"] = f"Satisfy {urgent_need.value}"
            state["should_replan"] = True
            state["reasoning_trace"].append(f"  → New goal: {state['current_goal']}")
        
        return state
    
    def plan_node(self, state: AgentState) -> AgentState:
        """Create or update plan"""
        state["reasoning_trace"].append(f"[PLAN] Creating plan for goal: {state['current_goal']}")
        state["current_status"] = "planning"
        
        # Use existing planner
        urgent_need = self.npc.needs.get_most_urgent_need()
        if urgent_need:
            plan = self.npc.planner.create_need_satisfaction_plan(
                urgent_need.value,
                self.npc.current_location
            )
            self.npc.planner.add_plan(plan)
            
            state["current_plan"] = {
                "goal": plan.goal,
                "steps": [{"action": s.action.value, "target": s.target} for s in plan.steps],
                "priority": plan.priority
            }
            state["plan_step"] = 0
            state["should_replan"] = False
            state["reasoning_trace"].append(f"  → Created plan with {len(plan.steps)} steps")
        
        return state
    
    def decide_node(self, state: AgentState) -> AgentState:
        """Decide what to do next"""
        state["reasoning_trace"].append(f"[DECIDE] Choosing action...")
        
        # Check if we need to plan
        if state["should_replan"] or (state["current_goal"] and not state["current_plan"]):
            state["next_node"] = "plan"
        
        # Check if we have messages to send
        elif state["messages_outbox"]:
            state["next_node"] = "communicate"
        
        # Execute current plan
        elif state["current_plan"]:
            state["next_node"] = "act"
        
        # Nothing to do
        else:
            state["next_node"] = "end"
        
        state["reasoning_trace"].append(f"  → Decision: {state['next_node']}")
        return state
    
    def route_after_decision(self, state: AgentState) -> Literal["plan", "act", "communicate", "end"]:
        """Router function for conditional edges"""
        return state.get("next_node", "end")

    def act_node(self, state: AgentState) -> AgentState:
        """Execute action"""
        state["reasoning_trace"].append(f"[ACT] Executing action...")
        state["current_status"] = "acting"

        # Execute NPC's autonomous tick
        action_description = self.npc.autonomous_tick()

        state["last_action"] = action_description
        state["action_result"] = ActionResult(
            success=True,
            description=action_description,
            effects={}
        )

        # Update state from NPC
        state["location"] = self.npc.current_location

        # Advance plan step if we have a plan
        if state["current_plan"]:
            state["plan_step"] += 1

        state["reasoning_trace"].append(f"  → Action: {action_description}")
        state["internal_monologue"].append(f"I {action_description}")

        return state

    def reflect_node(self, state: AgentState) -> AgentState:
        """Reflect on action outcome and learn"""
        state["reasoning_trace"].append(f"[REFLECT] Evaluating results...")

        # Check if action was successful
        if state["action_result"] and state["action_result"].success:
            state["reasoning_trace"].append("  → Action succeeded")

            # If plan is complete, clear goal
            if state["current_plan"]:
                steps = state["current_plan"].get("steps", [])
                if state["plan_step"] >= len(steps):
                    state["current_goal"] = None
                    state["current_plan"] = None
                    state["reasoning_trace"].append("  → Goal achieved!")
        else:
            state["reasoning_trace"].append("  → Action failed, need to replan")
            state["should_replan"] = True

        state["iteration_count"] += 1
        return state

    def communicate_node(self, state: AgentState) -> AgentState:
        """Handle communication with other agents"""
        state["reasoning_trace"].append(f"[COMMUNICATE] Processing messages...")
        state["current_status"] = "communicating"

        # Process outbox
        if state["messages_outbox"]:
            msg = state["messages_outbox"][0]
            state["reasoning_trace"].append(f"  → Sending message to {msg.to_agent}: {msg.content}")
            state["messages_outbox"] = state["messages_outbox"][1:]  # Remove sent message

        # Process inbox
        if state["messages_inbox"]:
            msg = state["messages_inbox"][-1]  # Get most recent
            state["reasoning_trace"].append(f"  → Received from {msg.from_agent}: {msg.content}")

        return state

    # ===== PUBLIC API =====

    def step(self, world_state: dict = None) -> AgentState:
        """Execute one step of the agent's decision cycle"""

        # Update state with world info
        if world_state:
            self.state["world_state"] = world_state
            self.state["nearby_npcs"] = world_state.get("nearby_npcs", [])

        self.state["tick"] += 1

        # Run the graph
        result = self.app.invoke(self.state)

        # Update internal state
        self.state = result

        return result

    def send_message(self, to_agent: str, message_type: str, content: str, priority: int = 5):
        """Queue a message to send to another agent"""
        msg = Message(
            from_agent=self.state["npc_name"],
            to_agent=to_agent,
            message_type=message_type,
            content=content,
            priority=priority
        )
        self.state["messages_outbox"].append(msg)

    def receive_message(self, message: Message):
        """Receive a message from another agent"""
        self.state["messages_inbox"].append(message)

    def get_reasoning_trace(self) -> list[str]:
        """Get the agent's reasoning trace for debugging"""
        return self.state.get("reasoning_trace", [])

    def get_internal_monologue(self) -> list[str]:
        """Get the agent's internal thoughts"""
        return self.state.get("internal_monologue", [])
