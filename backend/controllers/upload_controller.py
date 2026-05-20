from fastapi import UploadFile
from models import UploadResponse, DocumentType
from services import DocumentService, SessionService
from rag import RAGPipeline
from core.exceptions import UnsupportedFileTypeError


class UploadController:
    def __init__(
        self,
        document_service: DocumentService,
        session_service: SessionService,
        rag_pipeline: RAGPipeline,
    ):
        self._doc_svc = document_service
        self._session_svc = session_service
        self._rag = rag_pipeline

    async def upload_document(
        self,
        file: UploadFile,
        session_id: str,
        doc_type: DocumentType,
    ) -> UploadResponse:
        filename = file.filename or "upload"
        if not (filename.lower().endswith(".pdf") or filename.lower().endswith(".txt")):
            raise UnsupportedFileTypeError(filename)

        raw_bytes = await file.read()
        text = self._doc_svc.parse(raw_bytes, filename)
        chunks_stored = self._rag.ingest(session_id, doc_type.value, text)
        self._session_svc.update_document(session_id, doc_type.value, text)

        return UploadResponse(
            session_id=session_id,
            document_type=doc_type,
            filename=filename,
            chunks_stored=chunks_stored,
            message=f"{doc_type.value.upper()} uploaded and indexed successfully.",
        )
