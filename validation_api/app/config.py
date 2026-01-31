import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_ID: str = "dear-arte"
    LOCATION: str = "us-central1"
    BUCKET_NAME: str = "content_review_dear_arte"
    GOOGLE_APPLICATION_CREDENTIALS: str = ""  # Empty for Cloud Run - uses service account

    class Config:
        env_file = ".env"

settings = Settings()
