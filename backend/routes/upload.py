from fastapi import APIRouter, UploadFile, File, Form, Depends
from models import UploadResponse, DocumentType
from controllers import UploadController
from services import DocumentService, SessionService
from rag import RAGPipeline
from core.dependencies import (
    get_document_service,
    get_session_service,
    get_embedding_service,
    get_vector_store_service,
)
from config import get_settings

router = APIRouter(prefix="/upload", tags=["Upload"])


def _get_upload_controller(
    doc_svc: DocumentService = Depends(get_document_service),
    session_svc: SessionService = Depends(get_session_service),
    embedding_svc=Depends(get_embedding_service),
    vector_store=Depends(get_vector_store_service),
) -> UploadController:
    pipeline = RAGPipeline(embedding_svc, vector_store)
    return UploadController(doc_svc, session_svc, pipeline)


@router.post("/resume", response_model=UploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    session_id: str = Form(...),
    controller: UploadController = Depends(_get_upload_controller),
) -> UploadResponse:
    return await controller.upload_document(file, session_id, DocumentType.resume)


@router.post("/jd", response_model=UploadResponse)
async def upload_jd(
    file: UploadFile = File(...),
    session_id: str = Form(...),
    controller: UploadController = Depends(_get_upload_controller),
) -> UploadResponse:
    return await controller.upload_document(file, session_id, DocumentType.jd)
