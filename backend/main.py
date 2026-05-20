from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload_router, rag_router, interview_router, feedback_router
from config import get_settings

settings = get_settings()

app = FastAPI(
    title="AI Interview Preparation Assistant",
    description="RAG-based AI platform for technical interview preparation using LangGraph and Groq.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(rag_router)
app.include_router(interview_router)
app.include_router(feedback_router)


@app.api_route("/", methods=["GET", "HEAD"], tags=["Health"])
def health_check() -> dict:
    return {"status": "ok", "service": "AI Interview Preparation Assistant"}


@app.api_route("/health", methods=["GET", "HEAD"], tags=["Health"])
def health() -> dict:
    return {"status": "healthy"}
