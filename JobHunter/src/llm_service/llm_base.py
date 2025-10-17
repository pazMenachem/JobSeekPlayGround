"""Abstract interface for LLM providers."""

from abc import ABC, abstractmethod

class LLMInterface(ABC):
    """Abstract base class for LLM providers.
    
    This interface allows easy switching between different LLM providers
    (Ollama, OpenAI, Gemini, etc.) without changing the rest of the code.
    """
    
    @abstractmethod
    def send_to_llm(self, message: str) -> str:
        """Send a message to the LLM and get the raw response.
        
        Args:
            message: The message to send to the LLM
            
        Returns:
            Raw response from the LLM (JSON string for LLM processing)
        """
        pass

    @abstractmethod
    def _setup(self) -> None:
        """Setup the LLM provider."""
        pass
    