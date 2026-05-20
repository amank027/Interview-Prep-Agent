import chromadb
from chromadb.config import Settings


class VectorStoreService:
    def __init__(self, persist_dir: str = "./chroma_db"):
        self._client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )

    def _collection_name(self, session_id: str, doc_type: str) -> str:
        return f"{session_id}_{doc_type}"

    def store(
        self,
        session_id: str,
        doc_type: str,
        chunks: list[str],
        embeddings: list[list[float]],
    ) -> int:
        name = self._collection_name(session_id, doc_type)
        # Delete existing collection if it exists to allow re-upload
        try:
            self._client.delete_collection(name)
        except Exception:
            pass

        collection = self._client.create_collection(name)
        ids = [f"{name}_{i}" for i in range(len(chunks))]
        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
        )
        return len(chunks)

    def retrieve(
        self,
        session_id: str,
        doc_types: list[str],
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:
        results = []
        for doc_type in doc_types:
            name = self._collection_name(session_id, doc_type)
            try:
                collection = self._client.get_collection(name)
            except Exception:
                continue

            response = collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, collection.count()),
                include=["documents", "distances"],
            )
            docs = response["documents"][0]
            distances = response["distances"][0]
            for doc, dist in zip(docs, distances):
                results.append(
                    {
                        "content": doc,
                        "source": doc_type,
                        "score": round(1 - dist, 4),
                    }
                )

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def collection_exists(self, session_id: str, doc_type: str) -> bool:
        name = self._collection_name(session_id, doc_type)
        try:
            self._client.get_collection(name)
            return True
        except Exception:
            return False
