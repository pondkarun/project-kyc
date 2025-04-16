from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 8000
    reload: bool = False
    database_url: str
    base_image_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

settings = Settings()