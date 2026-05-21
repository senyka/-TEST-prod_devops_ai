"""Domain events for the DevOps AI Agent."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
import uuid


class EventType(Enum):
    """Types of domain events."""
    # Agent events
    AGENT_CREATED = "agent.created"
    AGENT_STARTED = "agent.started"
    AGENT_STOPPED = "agent.stopped"
    AGENT_ERROR = "agent.error"
    
    # Task events
    TASK_CREATED = "task.created"
    TASK_STARTED = "task.started"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    TASK_CANCELLED = "task.cancelled"
    
    # Plan events
    PLAN_CREATED = "plan.created"
    PLAN_UPDATED = "plan.updated"
    PLAN_EXECUTED = "plan.executed"
    
    # Step events
    STEP_STARTED = "step.started"
    STEP_COMPLETED = "step.completed"
    STEP_FAILED = "step.failed"
    
    # Tool events
    TOOL_INVOKED = "tool.invoked"
    TOOL_COMPLETED = "tool.completed"
    TOOL_ERROR = "tool.error"
    
    # General events
    MESSAGE_RECEIVED = "message.received"
    MESSAGE_SENT = "message.sent"


@dataclass
class DomainEvent:
    """Base class for all domain events."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = EventType.MESSAGE_RECEIVED
    timestamp: datetime = field(default_factory=datetime.utcnow)
    aggregate_id: Optional[str] = None
    aggregate_type: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "data": self.data,
            "metadata": self.metadata,
        }


@dataclass
class AgentEvent(DomainEvent):
    """Event related to agent lifecycle."""
    agent_id: str = ""
    agent_name: str = ""
    status: str = ""
    
    def __post_init__(self):
        self.aggregate_id = self.agent_id
        self.aggregate_type = "Agent"


@dataclass
class TaskEvent(DomainEvent):
    """Event related to task lifecycle."""
    task_id: str = ""
    task_name: str = ""
    status: str = ""
    
    def __post_init__(self):
        self.aggregate_id = self.task_id
        self.aggregate_type = "Task"


@dataclass
class PlanEvent(DomainEvent):
    """Event related to plan lifecycle."""
    plan_id: str = ""
    goal: str = ""
    status: str = ""
    
    def __post_init__(self):
        self.aggregate_id = self.plan_id
        self.aggregate_type = "Plan"


@dataclass
class StepEvent(DomainEvent):
    """Event related to step execution."""
    step_id: str = ""
    plan_id: str = ""
    description: str = ""
    status: str = ""
    result: Optional[str] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        self.aggregate_id = self.step_id
        self.aggregate_type = "Step"


@dataclass
class ToolEvent(DomainEvent):
    """Event related to tool invocation."""
    tool_id: str = ""
    tool_name: str = ""
    action: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        self.aggregate_id = self.tool_id
        self.aggregate_type = "Tool"


__all__ = [
    "EventType",
    "DomainEvent",
    "AgentEvent",
    "TaskEvent",
    "PlanEvent",
    "StepEvent",
    "ToolEvent",
]
