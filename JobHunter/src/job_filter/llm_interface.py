"""Abstract interface for LLM providers."""

from abc import ABC, abstractmethod
from src.data_models import JobData


class LLMInterface(ABC):
    """Abstract base class for LLM providers.
    
    This interface allows easy switching between different LLM providers
    (Ollama, OpenAI, Gemini, etc.) without changing the rest of the code.
    """
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the LLM service is available.
        
        Returns:
            True if the service is available, False otherwise
        """
        pass
    
    @abstractmethod
    def generate_response(self, **kwargs) -> str:
        """Generate a response from the LLM.
        
        Args:
            **kwargs: Parameters for the LLM call, including 'prompt'
            
        Returns:
            Generated response from the LLM
        """
        pass
    
    @abstractmethod
    def analyze_job_relevance(self, job_data: JobData, prompt: str) -> str:
        """Analyze job relevance using the LLM.
        
        Args:
            job_data: JobData object containing job information
            prompt: The prompt to send to the LLM
            
        Returns:
            Simple one-word response: 'yes', 'no', or 'maybe'
        """
        pass
