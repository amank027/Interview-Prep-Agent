from pydantic import BaseModel
from enum import Enum


class InterviewType(str, Enum):
    technical = "technical"
    behavioral = "behavioral"
    mixed = "mixed"


class StartInterviewRequest(BaseModel):
    session_id: str
    interview_type: InterviewType = InterviewType.technical
    num_questions: int = 5


class StartInterviewResponse(BaseModel):
    session_id: str
    interview_id: str
    first_question: str
    total_questions: int
    message: str


class AnswerRequest(BaseModel):
    session_id: str
    interview_id: str
    answer: str


class AnswerResponse(BaseModel):
    session_id: str
    interview_id: str
    next_question: str | None
    is_complete: bool
    questions_answered: int
    total_questions: int
    message: str
