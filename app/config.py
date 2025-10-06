from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KEY: str
    REFRESH_KEY: str  
    ALGORITHM: str
    
    DB_URL : str
    
    class Config:
        env_file = ".env"
        
settings = Settings()