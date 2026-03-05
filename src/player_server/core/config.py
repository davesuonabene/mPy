from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "mPy - Media Server"
    DATABASE_URL: str = "sqlite:///./data/mpy_data.db"
    MUSIC_DIRECTORY: str = "./data/music"
    
    class Config:
        env_file = ".env"

settings = Settings()
