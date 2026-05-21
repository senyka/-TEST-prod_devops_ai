"""Application services for the DevOps AI Agent."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from src.domain.models.entities import Plan, Step, ActionResult, TaskStatus
from src.domain.events.events import DomainEvent


class LLMService(ABC):
    """
    Service interface for LLM interactions.
    
    This is the primary interface that application layer uses
    to interact with different LLM providers (OpenAI, Anthropic, Azure).
    """
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text
        """
        pass
    
    @abstractmethod
    def generate_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Generate text with tool calling capabilities.
        
        Args:
            prompt: The input prompt
            tools: List of available tools
            **kwargs: Additional generation parameters
            
        Returns:
            Dictionary with response and any tool calls
        """
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Chat with the model using conversation history.
        
        Args:
            messages: List of message dictionaries
            **kwargs: Additional parameters
            
        Returns:
            Response message
        """
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        pass


class PlanningService(ABC):
    """
    Service for creating and managing plans.
    
    Orchestrates the planning process using LLM and domain knowledge.
    """
    
    @abstractmethod
    def create_plan(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Plan:
        """
        Create a plan to achieve a goal.
        
        Args:
            goal: The goal to achieve
            context: Additional context for planning
            
        Returns:
            A Plan object
        """
        pass
    
    @abstractmethod
    def refine_plan(
        self,
        plan: Plan,
        feedback: str,
    ) -> Plan:
        """
        Refine an existing plan based on feedback.
        
        Args:
            plan: The plan to refine
            feedback: Feedback for refinement
            
        Returns:
            Refined Plan
        """
        pass
    
    @abstractmethod
    def validate_plan(self, plan: Plan) -> bool:
        """
        Validate a plan for correctness and feasibility.
        
        Args:
            plan: The plan to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass


class ExecutionService(ABC):
    """
    Service for executing plans and steps.
    
    Manages the execution lifecycle of plans.
    """
    
    @abstractmethod
    def execute_plan(self, plan: Plan) -> ActionResult:
        """
        Execute a complete plan.
        
        Args:
            plan: The plan to execute
            
        Returns:
            ActionResult of execution
        """
        pass
    
    @abstractmethod
    def execute_step(self, step: Step) -> ActionResult:
        """
        Execute a single step.
        
        Args:
            step: The step to execute
            
        Returns:
            ActionResult of execution
        """
        pass
    
    @abstractmethod
    def cancel_execution(self, plan_id: str) -> bool:
        """
        Cancel an ongoing execution.
        
        Args:
            plan_id: ID of the plan to cancel
            
        Returns:
            True if cancelled successfully
        """
        pass


class ReflectionService(ABC):
    """
    Service for reflection and learning.
    
    Analyzes results and generates insights for improvement.
    """
    
    @abstractmethod
    def analyze_result(
        self,
        plan: Plan,
        result: ActionResult,
    ) -> Dict[str, Any]:
        """
        Analyze the result of plan execution.
        
        Args:
            plan: The executed plan
            result: The result of execution
            
        Returns:
            Analysis dictionary
        """
        pass
    
    @abstractmethod
    def generate_learnings(
        self,
        analysis: Dict[str, Any],
    ) -> List[str]:
        """
        Generate learnings from analysis.
        
        Args:
            analysis: Analysis results
            
        Returns:
            List of learning statements
        """
        pass
    
    @abstractmethod
    def suggest_improvements(
        self,
        analysis: Dict[str, Any],
    ) -> List[str]:
        """
        Suggest improvements based on analysis.
        
        Args:
            analysis: Analysis results
            
        Returns:
            List of improvement suggestions
        """
        pass


class EventService(ABC):
    """
    Service for event publishing and subscribing.
    
    Handles domain events across the system.
    """
    
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        """
        Publish an event.
        
        Args:
            event: Event to publish
        """
        pass
    
    @abstractmethod
    def subscribe(
        self,
        event_type: str,
        handler: callable,
    ) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Type of event to subscribe to
            handler: Handler function
        """
        pass
    
    @abstractmethod
    def unsubscribe(
        self,
        event_type: str,
        handler: callable,
    ) -> None:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Type of event
            handler: Handler function to remove
        """
        pass


__all__ = [
    "LLMService",
    "PlanningService",
    "ExecutionService",
    "ReflectionService",
    "EventService",
]
