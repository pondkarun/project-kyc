from pydantic import BaseSettings

class Settings(BaseSettings):
    base_image_url: str

    class Config:
        env_file = ".env"

settings = Settings()
