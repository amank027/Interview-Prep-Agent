from functools import lru_cache
from services.document_service import DocumentService
from services.embedding_service import EmbeddingService
from services.vector_store_service import VectorStoreService
from services.session_service import SessionService
from config import get_settings


@lru_cache
def get_embedding_service() -> EmbeddingService:
    settings = get_settings()
    return EmbeddingService(model_name=settings.embedding_model)


@lru_cache
def get_vector_store_service() -> VectorStoreService:
    settings = get_settings()
    return VectorStoreService(persist_dir=settings.chroma_persist_dir)


@lru_cache
def get_session_service() -> SessionService:
    return SessionService()


def get_document_service() -> DocumentService:
    return DocumentService()
