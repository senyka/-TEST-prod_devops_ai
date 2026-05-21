"""Domain entities for the DevOps AI Agent."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class AgentStatus(Enum):
    """Status of an agent."""
    IDLE = "idle"
    THINKING = "thinking"
    PLANNING = "planning"
    ACTING = "acting"
    REFLECTING = "reflecting"
    REPORTING = "reporting"
    ERROR = "error"


class TaskStatus(Enum):
    """Status of a task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Entity:
    """Base entity class with ID and timestamps."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Agent(Entity):
    """Agent entity representing an autonomous AI agent."""
    name: str = ""
    description: str = ""
    status: AgentStatus = AgentStatus.IDLE
    capabilities: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @abstractmethod
    def plan(self, goal: str) -> "Plan":
        """Create a plan to achieve a goal."""
        pass
    
    @abstractmethod
    def act(self, plan: "Plan") -> "ActionResult":
        """Execute actions based on the plan."""
        pass
    
    @abstractmethod
    def reflect(self, result: "ActionResult") -> "Reflection":
        """Reflect on the results of actions."""
        pass
    
    @abstractmethod
    def report(self) -> str:
        """Generate a report of agent's activities."""
        pass


@dataclass
class Plan(Entity):
    """Plan entity containing steps to achieve a goal."""
    goal: str = ""
    steps: List["Step"] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Step(Entity):
    """Individual step in a plan."""
    description: str = ""
    action_type: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None


@dataclass
class ActionResult(Entity):
    """Result of executing an action."""
    success: bool = False
    output: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Reflection(Entity):
    """Reflection on agent's performance."""
    observations: List[str] = field(default_factory=list)
    learnings: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Tool(Entity):
    """Tool entity representing a capability."""
    name: str = ""
    description: str = ""
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)
    
    @abstractmethod
    def execute(self, **kwargs) -> ActionResult:
        """Execute the tool with given parameters."""
        pass


@dataclass
class Plugin(Entity):
    """Plugin entity for extending agent capabilities."""
    name: str = ""
    version: str = ""
    description: str = ""
    enabled: bool = True
    dependencies: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)

__all__ = [
    "AgentStatus",
    "TaskStatus",
    "Entity",
    "Agent",
    "Plan",
    "Step",
    "ActionResult",
    "Reflection",
    "Tool",
    "Plugin",
]
