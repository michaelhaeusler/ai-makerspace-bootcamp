"""Application configuration settings."""

import os
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    debug: bool = Field(default=True, env="DEBUG")
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    cors_origins: str = Field(default="http://localhost:3000", env="CORS_ORIGINS")
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    
    # Tavily Web Search
    tavily_api_key: str = Field(..., env="TAVILY_API_KEY")
    
    # Qdrant Vector Database
    qdrant_host: str = Field(default="localhost", env="QDRANT_HOST")
    qdrant_port: int = Field(default=6333, env="QDRANT_PORT")
    qdrant_api_key: str = Field(default="", env="QDRANT_API_KEY")
    
    # LangSmith (Optional)
    langchain_tracing_v2: bool = Field(default=True, env="LANGCHAIN_TRACING_V2")
    langchain_api_key: str = Field(default="", env="LANGCHAIN_API_KEY")
    langchain_project: str = Field(default="insurancelens", env="LANGCHAIN_PROJECT")
    
    # File Upload Settings
    max_upload_size: int = Field(default=50000000, env="MAX_UPLOAD_SIZE")  # 50MB
    upload_folder: str = Field(default="uploads", env="UPLOAD_FOLDER")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS origins string to list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
