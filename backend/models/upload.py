from pydantic import BaseModel
from enum import Enum


class DocumentType(str, Enum):
    resume = "resume"
    jd = "jd"


class UploadResponse(BaseModel):
    session_id: str
    document_type: DocumentType
    filename: str
    chunks_stored: int
    message: str
