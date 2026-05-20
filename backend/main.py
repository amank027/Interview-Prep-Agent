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

# Allow all origins if CORS_ORIGINS contains "*", else use the list
origins = settings.cors_origins
allow_all = "*" in origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all else origins,
    allow_credentials=False if allow_all else True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(rag_router)
app.include_router(interview_router)
app.include_router(feedback_router)


@app.get("/", tags=["Health"])
def health_check() -> dict:
    return {"status": "ok", "service": "AI Interview Preparation Assistant"}


@app.get("/health", tags=["Health"])
def health() -> dict:
    return {"status": "healthy"}
