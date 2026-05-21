"""Agent orchestrator for managing agent lifecycle and execution."""
from typing import Any, Dict, List, Optional
from src.domain.models.entities import Agent, Plan, ActionResult, AgentStatus
from src.domain.events.events import DomainEvent, EventType, AgentEvent
from src.application.services.interfaces import (
    LLMService,
    PlanningService,
    ExecutionService,
    ReflectionService,
    EventService,
)


class AgentOrchestrator:
    """
    Orchestrates agent operations.
    
    This is the main entry point for using agents in the application layer.
    It coordinates between different services and manages agent state.
    """
    
    def __init__(
        self,
        llm_service: LLMService,
        planning_service: PlanningService,
        execution_service: ExecutionService,
        reflection_service: ReflectionService,
        event_service: Optional[EventService] = None,
    ):
        self.llm_service = llm_service
        self.planning_service = planning_service
        self.execution_service = execution_service
        self.reflection_service = reflection_service
        self.event_service = event_service
        self._agents: Dict[str, Agent] = {}
        self._execution_history: List[Dict[str, Any]] = []
    
    def register_agent(self, agent: Agent) -> None:
        """
        Register an agent with the orchestrator.
        
        Args:
            agent: Agent to register
        """
        self._agents[agent.id] = agent
        self._emit_event(
            EventType.AGENT_CREATED,
            agent_id=agent.id,
            agent_name=agent.name,
        )
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """
        Get a registered agent by ID.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            Agent if found, None otherwise
        """
        return self._agents.get(agent_id)
    
    def list_agents(self) -> List[Agent]:
        """
        List all registered agents.
        
        Returns:
            List of agents
        """
        return list(self._agents.values())
    
    def execute_goal(
        self,
        agent_id: str,
        goal: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a goal with a specific agent.
        
        Args:
            agent_id: ID of the agent to use
            goal: Goal to achieve
            context: Additional context
            
        Returns:
            Dictionary with execution results
        """
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' not found")
        
        # Create plan
        agent.status = AgentStatus.PLANNING
        plan = self.planning_service.create_plan(goal, context)
        
        self._emit_event(
            EventType.PLAN_CREATED,
            agent_id=agent_id,
            data={"plan_id": plan.id, "goal": goal},
        )
        
        # Execute plan
        agent.status = AgentStatus.ACTING
        result = self.execution_service.execute_plan(plan)
        
        # Reflect on results
        agent.status = AgentStatus.REFLECTING
        analysis = self.reflection_service.analyze_result(plan, result)
        learnings = self.reflection_service.generate_learnings(analysis)
        improvements = self.reflection_service.suggest_improvements(analysis)
        
        # Generate report
        agent.status = AgentStatus.REPORTING
        report = self._generate_report(goal, plan, result, analysis)
        
        agent.status = AgentStatus.IDLE
        
        # Store execution history
        execution_record = {
            "agent_id": agent_id,
            "goal": goal,
            "plan": plan,
            "result": result,
            "analysis": analysis,
            "learnings": learnings,
            "improvements": improvements,
            "report": report,
        }
        self._execution_history.append(execution_record)
        
        return execution_record
    
    def _generate_report(
        self,
        goal: str,
        plan: Plan,
        result: ActionResult,
        analysis: Dict[str, Any],
    ) -> str:
        """
        Generate a human-readable report.
        
        Args:
            goal: The original goal
            plan: The executed plan
            result: The result of execution
            analysis: Analysis of results
            
        Returns:
            Formatted report string
        """
        lines = [
            "=" * 60,
            "EXECUTION REPORT",
            "=" * 60,
            f"Goal: {goal}",
            f"Plan ID: {plan.id}",
            f"Steps: {len(plan.steps)}",
            f"Status: {'Success' if result.success else 'Failed'}",
            "",
            "Execution Summary:",
            "-" * 40,
        ]
        
        for i, step in enumerate(plan.steps, 1):
            status = "✓" if step.status.value == "completed" else "✗"
            lines.append(f"  {status} Step {i}: {step.description}")
            if step.error:
                lines.append(f"      Error: {step.error}")
        
        lines.extend([
            "",
            "Analysis:",
            "-" * 40,
            str(analysis),
            "",
            "=" * 60,
        ])
        
        return "\n".join(lines)
    
    def get_execution_history(
        self,
        agent_id: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Get execution history.
        
        Args:
            agent_id: Filter by agent ID (optional)
            limit: Maximum number of records to return
            
        Returns:
            List of execution records
        """
        if agent_id:
            filtered = [
                e for e in self._execution_history
                if e.get("agent_id") == agent_id
            ]
            return filtered[-limit:]
        return self._execution_history[-limit:]
    
    def _emit_event(
        self,
        event_type: EventType,
        agent_id: str = "",
        agent_name: str = "",
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Emit an event if event service is available.
        
        Args:
            event_type: Type of event
            agent_id: Agent ID
            agent_name: Agent name
            data: Event data
        """
        if self.event_service:
            event = AgentEvent(
                event_type=event_type,
                agent_id=agent_id,
                agent_name=agent_name,
                data=data or {},
            )
            self.event_service.publish(event)


__all__ = ["AgentOrchestrator"]
