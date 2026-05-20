from models import RAGQueryRequest, RAGQueryResponse, RetrievedChunk
from services import SessionService, VectorStoreService
from rag import RAGPipeline
from core.exceptions import DocumentNotUploadedError


class RAGController:
    def __init__(
        self,
        session_service: SessionService,
        rag_pipeline: RAGPipeline,
        vector_store: VectorStoreService,
    ):
        self._session_svc = session_service
        self._rag = rag_pipeline
        self._store = vector_store

    def query(self, request: RAGQueryRequest) -> RAGQueryResponse:
        session = self._session_svc.get_or_create(request.session_id)

        available_docs = []
        if session.has_resume:
            available_docs.append("resume")
        if session.has_jd:
            available_docs.append("jd")

        if not available_docs:
            raise DocumentNotUploadedError("resume or JD")

        answer, chunks = self._rag.query(
            session_id=request.session_id,
            question=request.query,
            doc_types=available_docs,
            conversation_history=session.conversation_history,
        )

        self._session_svc.add_conversation_turn(request.session_id, "user", request.query)
        self._session_svc.add_conversation_turn(request.session_id, "assistant", answer)

        return RAGQueryResponse(
            session_id=request.session_id,
            query=request.query,
            answer=answer,
            retrieved_chunks=[
                RetrievedChunk(
                    content=c["content"],
                    source=c["source"],
                    score=c["score"],
                )
                for c in chunks
            ],
        )
