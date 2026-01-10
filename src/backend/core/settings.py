from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "AutoCode MD"
    VERSION: str = "0.1.0"
    
    # Paths
    DATA_PATH: str = "data/icd10_guidelines.pdf"
    
    # Vector DB Config (Docker Service)
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000
    COLLECTION_NAME: str = "icd10_rules"
    
    # Model Config
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    VISION_MODEL: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    CODING_MODEL: str = "llama-3.3-70b-versatile"

    GROQ_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "autocode"
    TABLE_NAME : str = "medical_notes"
    
    # Construct the Database URL
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

# Singleton instance
settings = Settings()