from pydantic_settings import BaseSettings

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

    GROQ_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"

# Singleton instance
settings = Settings()