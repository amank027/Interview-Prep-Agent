from services.embedding_service import EmbeddingService
from services.vector_store_service import VectorStoreService


class Retriever:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStoreService,
    ):
        self._embedder = embedding_service
        self._store = vector_store

    def retrieve(
        self,
        session_id: str,
        query: str,
        doc_types: list[str],
        top_k: int = 5,
    ) -> list[dict]:
        query_embedding = self._embedder.embed_single(query)
        return self._store.retrieve(
            session_id=session_id,
            doc_types=doc_types,
            query_embedding=query_embedding,
            top_k=top_k,
        )
