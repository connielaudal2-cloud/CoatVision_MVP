"""
Unit tests for Sparks service and API endpoints
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.sparks_service import SparksService, get_sparks_service


client = TestClient(app)


class TestSparksAPI:
    """Test Sparks API endpoints"""
    
    @patch('backend.app.services.sparks_service.openai.OpenAI')
    def test_health_endpoint(self, mock_openai_class):
        """Test Sparks health check endpoint"""
        # Mock the OpenAI client
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        response = client.get("/api/sparks/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "sparks"
        assert "model" in data
    
    @patch('backend.app.services.sparks_service.openai.OpenAI')
    @patch('backend.app.services.sparks_service.SparksService.generate_code')
    def test_generate_code_success(self, mock_generate, mock_openai_class):
        """Test successful code generation"""
        # Mock the OpenAI client
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        # Mock the generate_code method
        mock_generate.return_value = {
            "status": "success",
            "code": "print('Hello, World!')",
            "app_type": "web",
            "framework": "FastAPI",
            "timestamp": "2026-01-04T00:00:00",
            "model_used": "gpt-4o"
        }
        
        payload = {
            "description": "Create a simple hello world web application",
            "app_type": "web",
            "framework": "FastAPI"
        }
        
        response = client.post("/api/sparks/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "code" in data
        assert data["app_type"] == "web"
    
    def test_generate_code_missing_description(self):
        """Test code generation with missing description"""
        payload = {
            "app_type": "web"
        }
        
        response = client.post("/api/sparks/generate", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_generate_code_short_description(self):
        """Test code generation with too short description"""
        payload = {
            "description": "short",
            "app_type": "web"
        }
        
        response = client.post("/api/sparks/generate", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_generate_code_long_description(self):
        """Test code generation with too long description"""
        payload = {
            "description": "a" * 6000,  # Over 5000 character limit
            "app_type": "web"
        }
        
        response = client.post("/api/sparks/generate", json=payload)
        assert response.status_code == 422  # Validation error


class TestSparksService:
    """Test Sparks service logic"""
    
    @pytest.fixture
    def mock_openai_client(self):
        """Create a mock OpenAI client"""
        with patch('backend.app.services.sparks_service.openai.OpenAI') as mock:
            mock_client = Mock()
            mock_response = Mock()
            mock_choice = Mock()
            mock_message = Mock()
            
            mock_message.content = "Generated code here"
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            
            mock_client.chat.completions.create.return_value = mock_response
            mock.return_value = mock_client
            
            yield mock_client
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_service_initialization(self, mock_openai_client):
        """Test service initialization with API key"""
        service = SparksService()
        assert service.model is not None
    
    def test_service_initialization_no_api_key(self):
        """Test service initialization without API key fails"""
        with patch('backend.app.services.sparks_service.OPENAI_API_KEY', None):
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                SparksService()
    
    @pytest.mark.asyncio
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    async def test_validate_request_valid(self, mock_openai_client):
        """Test request validation with valid description"""
        service = SparksService()
        result = await service.validate_request("This is a valid description for code generation")
        assert result is True
    
    @pytest.mark.asyncio
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    async def test_validate_request_too_short(self, mock_openai_client):
        """Test request validation with too short description"""
        service = SparksService()
        with pytest.raises(ValueError, match="at least 10 characters"):
            await service.validate_request("short")
    
    @pytest.mark.asyncio
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    async def test_validate_request_too_long(self, mock_openai_client):
        """Test request validation with too long description"""
        service = SparksService()
        long_desc = "a" * 6000
        with pytest.raises(ValueError, match="too long"):
            await service.validate_request(long_desc)
    
    def test_build_prompt_basic(self):
        """Test prompt building with basic parameters"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('backend.app.services.sparks_service.openai.OpenAI'):
                service = SparksService()
                prompt = service._build_prompt(
                    description="Create a web app",
                    app_type="web",
                    framework=None,
                    additional_requirements=None
                )
                assert "Create a web app" in prompt
                assert "web application" in prompt
    
    def test_build_prompt_with_framework(self):
        """Test prompt building with framework specified"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('backend.app.services.sparks_service.openai.OpenAI'):
                service = SparksService()
                prompt = service._build_prompt(
                    description="Create a web app",
                    app_type="web",
                    framework="FastAPI",
                    additional_requirements=None
                )
                assert "FastAPI" in prompt
    
    def test_build_prompt_with_additional_requirements(self):
        """Test prompt building with additional requirements"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('backend.app.services.sparks_service.openai.OpenAI'):
                service = SparksService()
                prompt = service._build_prompt(
                    description="Create a web app",
                    app_type="web",
                    framework=None,
                    additional_requirements="Use PostgreSQL database"
                )
                assert "PostgreSQL database" in prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
