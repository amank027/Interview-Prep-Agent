from pydantic import BaseModel


class QuestionFeedback(BaseModel):
    question: str
    user_answer: str
    score: int
    strengths: list[str]
    improvements: list[str]
    ideal_answer_hints: str


class RoadmapItem(BaseModel):
    topic: str
    priority: str
    resources: list[str]
    estimated_time: str


class FeedbackResponse(BaseModel):
    session_id: str
    interview_id: str
    overall_score: int
    overall_summary: str
    question_feedbacks: list[QuestionFeedback]
    roadmap: list[RoadmapItem]
    strengths: list[str]
    areas_for_improvement: list[str]
