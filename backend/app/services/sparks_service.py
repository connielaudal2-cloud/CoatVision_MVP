"""
Sparks Service: Real-time code generation platform
Handles code generation requests using OpenAI integration
"""
import logging
import os
from typing import Dict, Optional
from datetime import datetime
import openai

from .config import OPENAI_API_KEY, OPENAI_MODEL

# Configure logging
logger = logging.getLogger(__name__)


class SparksService:
    """Service for handling code generation requests"""
    
    def __init__(self):
        """Initialize Sparks service with OpenAI client"""
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Create OpenAI client
        try:
            self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
            self.model = OPENAI_MODEL
            logger.info("SparksService initialized with model: %s", self.model)
        except Exception as e:
            logger.error("Failed to initialize OpenAI client: %s", str(e))
            raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")
    
    async def generate_code(
        self,
        description: str,
        app_type: str = "web",
        framework: Optional[str] = None,
        additional_requirements: Optional[str] = None
    ) -> Dict:
        """
        Generate code based on user requirements
        
        Args:
            description: Description of the app/system to generate
            app_type: Type of application (web, mobile, api, etc.)
            framework: Preferred framework (optional)
            additional_requirements: Additional requirements (optional)
        
        Returns:
            Dict containing generated code and metadata
        """
        try:
            # Build prompt for code generation
            prompt = self._build_prompt(
                description, app_type, framework, additional_requirements
            )
            
            logger.info("Generating code for app_type: %s", app_type)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert software developer. Generate clean, production-ready code based on user requirements."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            generated_code = response.choices[0].message.content
            
            logger.info("Code generation successful")
            
            return {
                "status": "success",
                "code": generated_code,
                "app_type": app_type,
                "framework": framework,
                "timestamp": datetime.utcnow().isoformat(),
                "model_used": self.model
            }
            
        except openai.APIError as e:
            logger.error("OpenAI API error: %s", str(e))
            raise ValueError(f"OpenAI API error: {str(e)}")
        except Exception as e:
            logger.error("Code generation failed: %s", str(e))
            raise ValueError(f"Code generation failed: {str(e)}")
    
    def _build_prompt(
        self,
        description: str,
        app_type: str,
        framework: Optional[str],
        additional_requirements: Optional[str]
    ) -> str:
        """Build the prompt for code generation"""
        prompt_parts = [
            f"Generate a {app_type} application with the following description:",
            f"\n{description}\n"
        ]
        
        if framework:
            prompt_parts.append(f"\nUse the {framework} framework.")
        
        if additional_requirements:
            prompt_parts.append(f"\nAdditional requirements:\n{additional_requirements}")
        
        prompt_parts.append("\nProvide clean, well-documented code with best practices.")
        
        return "".join(prompt_parts)
    
    async def validate_request(self, description: str) -> bool:
        """
        Validate code generation request
        
        Args:
            description: The description to validate
            
        Returns:
            True if valid, raises ValueError otherwise
        """
        if not description or len(description.strip()) < 10:
            raise ValueError("Description must be at least 10 characters")
        
        if len(description) > 5000:
            raise ValueError("Description too long (max 5000 characters)")
        
        return True


# Singleton instance
_sparks_service: Optional[SparksService] = None


def get_sparks_service() -> SparksService:
    """Get or create Sparks service instance"""
    global _sparks_service
    if _sparks_service is None:
        _sparks_service = SparksService()
    return _sparks_service
