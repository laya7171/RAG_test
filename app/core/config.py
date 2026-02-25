import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./rag.db")
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Pinecone Configuration
    PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX: str = os.getenv("PINECONE_INDEX", "rag-index")
    PINECONE_ENVIRONMENT: Optional[str] = os.getenv("PINECONE_ENVIRONMENT")
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Application Settings
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB
    CHAT_HISTORY_TTL: int = int(os.getenv("CHAT_HISTORY_TTL", "86400"))  # 24 hours
    ALLOWED_EXTENSIONS: tuple = ('.pdf', '.txt')
    
    def validate(self) -> None:
        """Validate that all required settings are configured.
        
        Raises:
            ValueError: If any required setting is missing or invalid.
        """
        if not self.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY environment variable is required")
        
        if not self.PINECONE_INDEX:
            raise ValueError("PINECONE_INDEX environment variable is required")


# Global settings instance
settings = Settings()

if os.getenv("SKIP_SETTINGS_VALIDATION") != "true":
    try:
        settings.validate()
    except ValueError as e:
        print(f"Warning: Configuration validation: {e}")