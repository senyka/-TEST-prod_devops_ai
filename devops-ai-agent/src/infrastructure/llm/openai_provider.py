"""OpenAI LLM provider implementation."""
from typing import Any, Dict, List, Optional
from src.application.services.interfaces import LLMService


class OpenAIProvider(LLMService):
    """
    OpenAI LLM provider.
    
    Implements the LLMService interface for OpenAI models.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4",
        base_url: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._client = None
    
    @property
    def client(self):
        """Lazy initialization of OpenAI client."""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                )
            except ImportError:
                raise ImportError(
                    "Please install openai package: pip install openai"
                )
        return self._client
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from a prompt."""
        params = {
            "model": kwargs.get("model", self.model),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            **kwargs,
        }
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            **params,
        )
        
        return response.choices[0].message.content
    
    def generate_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        **kwargs,
    ) -> Dict[str, Any]:
        """Generate text with tool calling capabilities."""
        params = {
            "model": kwargs.get("model", self.model),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            **kwargs,
        }
        
        # Convert tools to OpenAI format
        openai_tools = self._convert_tools(tools)
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            tools=openai_tools,
            **params,
        )
        
        message = response.choices[0].message
        
        result = {
            "content": message.content,
            "tool_calls": [],
        }
        
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result["tool_calls"].append({
                    "id": tool_call.id,
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments,
                })
        
        return result
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat with the model using conversation history."""
        params = {
            "model": kwargs.get("model", self.model),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            **kwargs,
        }
        
        response = self.client.chat.completions.create(
            messages=messages,
            **params,
        )
        
        return response.choices[0].message.content
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        try:
            import tiktoken
            encoding = tiktoken.encoding_for_model(self.model)
            return len(encoding.encode(text))
        except ImportError:
            # Fallback: rough estimate
            return len(text.split()) * 1.3
    
    def _convert_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tools to OpenAI format."""
        openai_tools = []
        for tool in tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool.get("name", ""),
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {}),
                },
            }
            openai_tools.append(openai_tool)
        return openai_tools


__all__ = ["OpenAIProvider"]