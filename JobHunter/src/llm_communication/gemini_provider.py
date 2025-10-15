"""Gemini Flash API provider for batch job filtering."""

import os
import google.generativeai as genai
from src.logger import get_logger
from .llm_interface import LLMInterface
from src.config import llm_settings


class GeminiProvider(LLMInterface):
    """Gemini Flash API provider for batch job analysis.
    
    This provider uses Google's Gemini Flash API to analyze multiple jobs
    in a single batch request, providing efficient and cost-effective filtering.
    """
    
    def __init__(self) -> None:
        """Initialize the Gemini provider."""
        self.logger = get_logger("gemini_provider")
        self.model = None

        try:
            api_key = os.getenv("GEMINI_API_KEY")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(llm_settings.llm_model)
        
        except Exception as e:
            raise RuntimeError(f"Error initializing Gemini provider: {e}")
        
        self.logger.info("Gemini provider initialized")
    
    def send_to_llm(self, prompt: str) -> str:
        """Send a prompt to the Gemini API and get the raw response.

        Args:
            prompt: The prompt to send to the LLM

        Returns:
            Raw response from the LLM (JSON string for batch processing)
        """
        self.logger.debug("Sending batch prompt to Gemini API")
        
        response = self.model.generate_content(prompt)
        
        if not response.text:
            raise RuntimeError("Empty response from Gemini API")
        
        self.logger.debug(f"Received response from Gemini: {response.text}")
        return response.text
    
