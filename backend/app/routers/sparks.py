"""
Sparks API Router: Endpoints for code generation
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
import logging

from ..services.sparks_service import get_sparks_service, SparksService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/sparks", tags=["sparks"])


class CodeGenerationRequest(BaseModel):
    """Request model for code generation"""
    description: str = Field(..., min_length=10, max_length=5000, description="Description of the app/system to generate")
    app_type: str = Field(default="web", description="Type of application (web, mobile, api, etc.)")
    framework: Optional[str] = Field(None, description="Preferred framework (optional)")
    additional_requirements: Optional[str] = Field(None, max_length=2000, description="Additional requirements")


class CodeGenerationResponse(BaseModel):
    """Response model for code generation"""
    status: str
    code: str
    app_type: str
    framework: Optional[str]
    timestamp: str
    model_used: str


@router.post("/generate", response_model=CodeGenerationResponse)
async def generate_code(
    request: CodeGenerationRequest,
    sparks_service: SparksService = Depends(get_sparks_service)
):
    """
    Generate code based on user requirements
    
    - **description**: Detailed description of what to build
    - **app_type**: Type of application (web, mobile, api, etc.)
    - **framework**: Preferred framework (optional)
    - **additional_requirements**: Extra requirements (optional)
    """
    try:
        # Validate request
        await sparks_service.validate_request(request.description)
        
        # Generate code
        result = await sparks_service.generate_code(
            description=request.description,
            app_type=request.app_type,
            framework=request.framework,
            additional_requirements=request.additional_requirements
        )
        
        return result
        
    except ValueError as e:
        logger.warning("Validation error: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Code generation error: %s", str(e))
        raise HTTPException(status_code=500, detail="Code generation failed")


@router.get("/health")
async def health_check():
    """
    Health check endpoint for Sparks service
    """
    try:
        service = get_sparks_service()
        return {
            "status": "healthy",
            "service": "sparks",
            "model": service.model
        }
    except Exception as e:
        logger.error("Health check failed: %s", str(e))
        raise HTTPException(status_code=503, detail="Service unavailable")
