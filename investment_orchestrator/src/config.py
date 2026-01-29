"""Configuration management for Investment Orchestrator.

This module handles all configuration settings using environment variables
with sensible defaults for development and production environments.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""
    
    # Java Backend Configuration
    JAVA_BACKEND_URL: str = os.getenv("JAVA_BACKEND_URL", "http://localhost:8080")
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Cache Configuration
    CACHE_DURATION_MINUTES: int = int(os.getenv("CACHE_DURATION_MINUTES", "5"))
    
    # Performance Configuration
    MAX_CONCURRENT_REQUESTS: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))
    REQUEST_TIMEOUT_SECONDS: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))
    
    # Application Configuration
    APP_NAME: str = os.getenv("APP_NAME", "investment-orchestrator")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
    
    @classmethod
    def get_base_api_url(cls) -> str:
        """Get the base API URL for Java backend."""
        return f"{cls.JAVA_BACKEND_URL}/api"


# Create a singleton instance
config = Config()
