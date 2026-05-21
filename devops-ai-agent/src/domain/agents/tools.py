"""Tool abstractions for the DevOps AI Agent."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from src.domain.models.entities import Tool, ActionResult


class BaseTool(Tool, ABC):
    """
    Abstract base tool that all tools must implement.
    
    Tools are the building blocks that give agents capabilities.
    Each tool wraps a specific infrastructure capability.
    """
    
    def __init__(
        self,
        name: str = "",
        description: str = "",
        config: Optional[Dict[str, Any]] = None,
        enabled: bool = True,
    ):
        super().__init__(
            name=name,
            description=description,
            enabled=enabled,
            config=config or {},
        )
    
    @abstractmethod
    def execute(self, **kwargs) -> ActionResult:
        """
        Execute the tool with given parameters.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            ActionResult containing the outcome
        """
        pass
    
    def validate(self, **kwargs) -> bool:
        """
        Validate input parameters before execution.
        
        Args:
            **kwargs: Parameters to validate
            
        Returns:
            True if valid, False otherwise
        """
        return True
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the tool's parameter schema.
        
        Returns:
            Dictionary describing expected parameters
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {},
        }


class DevOpsTool(BaseTool, ABC):
    """
    Base class for DevOps-specific tools.
    
    Provides common functionality for Docker, Kubernetes, Terraform, etc.
    """
    
    def __init__(
        self,
        name: str = "",
        description: str = "",
        config: Optional[Dict[str, Any]] = None,
        requires_auth: bool = False,
        sandbox_mode: bool = True,
    ):
        super().__init__(name=name, description=description, config=config or {})
        self.requires_auth = requires_auth
        self.sandbox_mode = sandbox_mode
    
    @abstractmethod
    def check_prerequisites(self) -> bool:
        """
        Check if all prerequisites are met.
        
        Returns:
            True if ready to execute, False otherwise
        """
        pass
    
    def execute_safe(self, **kwargs) -> ActionResult:
        """
        Execute the tool in safe mode with validation.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            ActionResult containing the outcome
        """
        if not self.enabled:
            return ActionResult(
                success=False,
                error=f"Tool '{self.name}' is disabled",
            )
        
        if self.requires_auth and not self._check_auth():
            return ActionResult(
                success=False,
                error=f"Tool '{self.name}' requires authentication",
            )
        
        if not self.check_prerequisites():
            return ActionResult(
                success=False,
                error=f"Prerequisites not met for tool '{self.name}'",
            )
        
        if not self.validate(**kwargs):
            return ActionResult(
                success=False,
                error=f"Invalid parameters for tool '{self.name}'",
            )
        
        try:
            return self.execute(**kwargs)
        except Exception as e:
            return ActionResult(
                success=False,
                error=str(e),
            )
    
    def _check_auth(self) -> bool:
        """Check authentication status."""
        # Default implementation - override in subclasses
        return True


class GitTool(DevOpsTool, ABC):
    """Base class for Git-related tools (GitHub, GitLab)."""
    
    def __init__(
        self,
        name: str = "",
        description: str = "",
        config: Optional[Dict[str, Any]] = None,
        repo_url: str = "",
        branch: str = "main",
    ):
        super().__init__(name=name, description=description, config=config or {})
        self.repo_url = repo_url
        self.branch = branch
    
    @abstractmethod
    def clone(self, path: str) -> ActionResult:
        """Clone a repository."""
        pass
    
    @abstractmethod
    def commit(self, message: str, files: List[str]) -> ActionResult:
        """Commit changes."""
        pass
    
    @abstractmethod
    def push(self) -> ActionResult:
        """Push changes to remote."""
        pass


class ContainerTool(DevOpsTool, ABC):
    """Base class for container-related tools (Docker, K8s)."""
    
    def __init__(
        self,
        name: str = "",
        description: str = "",
        config: Optional[Dict[str, Any]] = None,
        namespace: str = "default",
    ):
        super().__init__(name=name, description=description, config=config or {})
        self.namespace = namespace
    
    @abstractmethod
    def build(self, context: str, tags: List[str]) -> ActionResult:
        """Build a container image."""
        pass
    
    @abstractmethod
    def deploy(self, manifest: Dict[str, Any]) -> ActionResult:
        """Deploy a container."""
        pass
    
    @abstractmethod
    def logs(self, container_id: str) -> ActionResult:
        """Get container logs."""
        pass


class IaCTool(DevOpsTool, ABC):
    """Base class for Infrastructure as Code tools (Terraform, Ansible)."""
    
    def __init__(
        self,
        name: str = "",
        description: str = "",
        config: Optional[Dict[str, Any]] = None,
        working_dir: str = ".",
        state_backend: str = "local",
    ):
        super().__init__(name=name, description=description, config=config or {})
        self.working_dir = working_dir
        self.state_backend = state_backend
    
    @abstractmethod
    def init(self) -> ActionResult:
        """Initialize the IaC workspace."""
        pass
    
    @abstractmethod
    def plan(self) -> ActionResult:
        """Create an execution plan."""
        pass
    
    @abstractmethod
    def apply(self, auto_approve: bool = False) -> ActionResult:
        """Apply the configuration."""
        pass
    
    @abstractmethod
    def destroy(self, auto_approve: bool = False) -> ActionResult:
        """Destroy resources."""
        pass


__all__ = [
    "BaseTool",
    "DevOpsTool",
    "GitTool",
    "ContainerTool",
    "IaCTool",
]
