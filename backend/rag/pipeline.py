from config import get_settings
from services.embedding_service import EmbeddingService
from services.vector_store_service import VectorStoreService
from services.llm_service import generate
from rag.chunker import TextChunker
from rag.retriever import Retriever


class RAGPipeline:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStoreService,
    ):
        settings = get_settings()
        self._chunker = TextChunker(
            chunk_size=settings.max_chunk_size,
            overlap=settings.chunk_overlap,
        )
        self._retriever = Retriever(embedding_service, vector_store)
        self._embedder = embedding_service
        self._store = vector_store
        self._top_k = settings.retrieval_top_k

    def ingest(self, session_id: str, doc_type: str, text: str) -> int:
        chunks = self._chunker.chunk(text)
        embeddings = self._embedder.embed(chunks)
        return self._store.store(session_id, doc_type, chunks, embeddings)

    def query(
        self,
        session_id: str,
        question: str,
        doc_types: list[str],
        system_context: str = "",
        conversation_history: list[dict] | None = None,
    ) -> tuple[str, list[dict]]:
        chunks = self._retriever.retrieve(
            session_id=session_id,
            query=question,
            doc_types=doc_types,
            top_k=self._top_k,
        )

        context = "\n\n".join(c["content"] for c in chunks)
        history_text = ""
        if conversation_history:
            history_lines = [
                f"{turn['role'].capitalize()}: {turn['content']}"
                for turn in conversation_history[-6:]
            ]
            history_text = "\n".join(history_lines)

        prompt = f"""You are an expert AI interview coach.

{system_context}

Context from documents:
{context}

{f"Conversation history:{chr(10)}{history_text}" if history_text else ""}

User question: {question}

Answer clearly and concisely based on the context provided."""

        answer = generate(prompt)
        return answer, chunks
