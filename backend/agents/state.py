from typing import TypedDict, Annotated
import operator


class AgentState(TypedDict):
    session_id: str
    task: str
    resume_text: str
    jd_text: str
    interview_type: str
    num_questions: int
    conversation_history: list[dict]
    current_question: str
    user_answer: str
    questions: list[str]
    retrieved_chunks: list[dict]
    analysis: str
    feedback: dict
    overall_feedback: dict
    roadmap: list[dict]
    error: str
    messages: Annotated[list[str], operator.add]
