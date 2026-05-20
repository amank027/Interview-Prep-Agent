from fastapi import APIRouter, Depends
from models import RAGQueryRequest, RAGQueryResponse
from controllers import RAGController
from services import SessionService
from rag import RAGPipeline
from core.dependencies import (
    get_session_service,
    get_embedding_service,
    get_vector_store_service,
)

router = APIRouter(prefix="/rag", tags=["RAG"])


def _get_rag_controller(
    session_svc: SessionService = Depends(get_session_service),
    embedding_svc=Depends(get_embedding_service),
    vector_store=Depends(get_vector_store_service),
) -> RAGController:
    pipeline = RAGPipeline(embedding_svc, vector_store)
    return RAGController(session_svc, pipeline, vector_store)


@router.post("/query", response_model=RAGQueryResponse)
def rag_query(
    request: RAGQueryRequest,
    controller: RAGController = Depends(_get_rag_controller),
) -> RAGQueryResponse:
    return controller.query(request)
