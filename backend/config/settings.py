from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    gemini_api_key: str = ""
    groq_api_key: str
    groq_model: str = "openai/gpt-oss-20b"
    chroma_persist_dir: str = "./chroma_db"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    max_chunk_size: int = 500
    chunk_overlap: int = 50
    retrieval_top_k: int = 5
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
