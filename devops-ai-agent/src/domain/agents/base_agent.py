"""Base agent implementation for the DevOps AI Agent."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from src.domain.models.entities import (
    Agent,
    Plan,
    Step,
    ActionResult,
    Reflection,
    AgentStatus,
    TaskStatus,
)
from src.domain.events.events import DomainEvent, EventType, AgentEvent


class BaseAgent(Agent, ABC):
    """
    Abstract base agent implementing the plan-act-reflect-report cycle.
    
    This is the core abstraction that all agent types must implement.
    Follows Clean Architecture principles with clear separation of concerns.
    """
    
    def __init__(
        self,
        name: str = "",
        description: str = "",
        capabilities: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            name=name,
            description=description,
            capabilities=capabilities or [],
            metadata=metadata or {},
        )
        self._events: List[DomainEvent] = []
    
    @abstractmethod
    def plan(self, goal: str) -> Plan:
        """
        Create a plan to achieve a goal.
        
        Args:
            goal: The goal to achieve
            
        Returns:
            A Plan object containing steps to achieve the goal
        """
        pass
    
    @abstractmethod
    def act(self, plan: Plan) -> ActionResult:
        """
        Execute actions based on the plan.
        
        Args:
            plan: The plan to execute
            
        Returns:
            ActionResult containing the outcome of execution
        """
        pass
    
    @abstractmethod
    def reflect(self, result: ActionResult) -> Reflection:
        """
        Reflect on the results of actions.
        
        Args:
            result: The result of action execution
            
        Returns:
            Reflection containing observations and learnings
        """
        pass
    
    @abstractmethod
    def report(self) -> str:
        """
        Generate a report of agent's activities.
        
        Returns:
            A string report of activities
        """
        pass
    
    def execute_cycle(self, goal: str) -> Dict[str, Any]:
        """
        Execute the full plan-act-reflect-report cycle.
        
        Args:
            goal: The goal to achieve
            
        Returns:
            Dictionary containing all results from the cycle
        """
        self.status = AgentStatus.PLANNING
        plan = self.plan(goal)
        
        self.status = AgentStatus.ACTING
        result = self.act(plan)
        
        self.status = AgentStatus.REFLECTING
        reflection = self.reflect(result)
        
        self.status = AgentStatus.REPORTING
        report = self.report()
        
        self.status = AgentStatus.IDLE
        
        return {
            "goal": goal,
            "plan": plan,
            "result": result,
            "reflection": reflection,
            "report": report,
        }
    
    def emit_event(self, event: DomainEvent) -> None:
        """
        Emit a domain event.
        
        Args:
            event: The event to emit
        """
        self._events.append(event)
    
    def get_events(self) -> List[DomainEvent]:
        """
        Get all emitted events.
        
        Returns:
            List of emitted events
        """
        return self._events.copy()
    
    def clear_events(self) -> None:
        """Clear all emitted events."""
        self._events.clear()
    
    def _emit_agent_event(
        self,
        event_type: EventType,
        status: str = "",
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Helper method to emit agent events.
        
        Args:
            event_type: Type of event
            status: Current status
            data: Additional event data
        """
        event = AgentEvent(
            event_type=event_type,
            agent_id=self.id,
            agent_name=self.name,
            status=status,
            data=data or {},
        )
        self.emit_event(event)
