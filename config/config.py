import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: str = ""
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()


print(f"Loaded OpenAI API Key (from settings): {settings.OPENAI_API_KEY[:5]}...{settings.OPENAI_API_KEY[-5:]}")
print(f"OpenAI API Key (from os.environ): {os.getenv('OPENAI_API_KEY')}")

print(f"Loaded OpenAI API Key (from settings): {settings.QDRANT_API_KEY[:5]}...{settings.QDRANT_API_KEY[-5:]}")
print(f"OpenAI API Key (from os.environ): {os.getenv('QDRANT_API_KEY')}")