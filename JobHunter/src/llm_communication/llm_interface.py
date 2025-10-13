"""Abstract interface for LLM providers."""

from abc import ABC, abstractmethod

class LLMInterface(ABC):
    """Abstract base class for LLM providers.
    
    This interface allows easy switching between different LLM providers
    (Ollama, OpenAI, Gemini, etc.) without changing the rest of the code.
    """

    @abstractmethod
    def is_available(self) -> None:
        """Check if the LLM service is available.
        
        raises:
            RuntimeError if the service is not available
        """
        response = self.send_to_llm("Hello")
        
        if response is None:
            raise RuntimeError("LLM service is not available")
    
    @abstractmethod
    def send_to_llm(self, prompt: str) -> str:
        """Send a prompt to the LLM and get the raw response.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            Raw response from the LLM (JSON string for batch processing)
        """
        pass
    