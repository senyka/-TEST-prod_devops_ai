# DevOps AI Agent

A plugin-based AI agent framework for DevOps automation, built with Clean Architecture and Domain-Driven Design principles.

## Features

- 🤖 **Plugin-based Agent System** - Extensible agent architecture with modular capabilities
- 🔄 **Event-driven Pipeline** - Asynchronous event processing for scalable operations
- 🔌 **Multiple LLM Providers** - Support for OpenAI, Anthropic, and Azure AI
- 🛠️ **DevOps Tools Integration** - Docker, Kubernetes, Terraform, GitHub, GitLab
- 📚 **RAG Capabilities** - Retrieval-Augmented Generation for knowledge-based tasks
- 🔒 **Security First** - Sandboxed execution and permission management
- 📊 **Observability** - Built-in metrics, tracing, and audit logging

## Architecture

```
devops-ai-agent/
├── src/
│   ├── domain/          # Business logic (Entities, Events, Services)
│   ├── application/     # Use cases and orchestrators
│   ├── infrastructure/  # External adapters (LLM, VCS, DevOps tools)
│   └── interface/       # API, CLI, Workers
├── examples/            # Usage examples
├── tests/               # Unit, integration, and e2e tests
└── docs/                # Documentation
```

## Installation

```bash
# Install base package
pip install devops-ai-agent

# Install with all features
pip install devops-ai-agent[dev]

# Install specific feature sets
pip install devops-ai-agent[llm]      # LLM providers
pip install devops-ai-agent[rag]      # RAG capabilities
pip install devops-ai-agent[vcs]      # Version control
pip install devops-ai-agent[devops]   # DevOps tools
pip install devops-ai-agent[api]      # FastAPI server
pip install devops-ai-agent[cli]      # Command-line interface
```

## Quick Start

```python
from src.domain.agents.base_agent import BaseAgent
from src.infrastructure.llm.openai_provider import OpenAIProvider
from src.application.orchestrators.agent_orchestrator import AgentOrchestrator

# Initialize LLM provider
llm = OpenAIProvider(api_key="your-api-key")

# Create and configure your agent
class MyDevOpsAgent(BaseAgent):
    def plan(self, goal: str):
        # Implement planning logic
        pass
    
    def act(self, plan):
        # Implement action execution
        pass
    
    def reflect(self, result):
        # Implement reflection
        pass
    
    def report(self):
        # Generate report
        pass

# Use the agent
agent = MyDevOpsAgent(name="DevOps Assistant")
orchestrator = AgentOrchestrator(...)
result = orchestrator.execute_goal(agent.id, "Deploy my application to Kubernetes")
```

## Examples

See the [`examples/`](examples/) directory for complete examples:

- `basic_agent/` - Simple agent implementation
- `rag_agent/` - Agent with RAG capabilities
- `devops_pipeline_agent/` - Full DevOps pipeline automation

## Development

```bash
# Clone the repository
git clone https://github.com/devops-ai-agent/devops-ai-agent.git
cd devops-ai-agent

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/
ruff check src/ tests/

# Type checking
mypy src/
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

We welcome contributions! Please see our contributing guidelines for more information.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
