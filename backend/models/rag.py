from pydantic import BaseModel


class RAGQueryRequest(BaseModel):
    session_id: str
    query: str


class RetrievedChunk(BaseModel):
    content: str
    source: str
    score: float


class RAGQueryResponse(BaseModel):
    session_id: str
    query: str
    answer: str
    retrieved_chunks: list[RetrievedChunk]
