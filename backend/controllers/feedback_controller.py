from models import FeedbackResponse, QuestionFeedback, RoadmapItem
from services import SessionService
from agents import interview_graph
from core.exceptions import InterviewNotFoundError, SessionNotFoundError


class FeedbackController:
    def __init__(self, session_service: SessionService):
        self._session_svc = session_service

    def get_feedback(self, session_id: str, interview_id: str) -> FeedbackResponse:
        session = self._session_svc.get_session(session_id)
        if session is None:
            raise SessionNotFoundError(session_id)

        interview = self._session_svc.get_interview(session_id, interview_id)
        if interview is None:
            raise InterviewNotFoundError(interview_id)

        question_feedbacks: list[QuestionFeedback] = []
        for question, answer in zip(interview.questions, interview.answers):
            result = interview_graph.invoke(
                {
                    "session_id": session_id,
                    "task": "feedback",
                    "resume_text": session.resume_text,
                    "jd_text": session.jd_text,
                    "current_question": question,
                    "user_answer": answer,
                    "questions": interview.questions,
                    "conversation_history": [],
                    "messages": [],
                }
            )
            fb = result.get("feedback", {})
            question_feedbacks.append(
                QuestionFeedback(
                    question=question,
                    user_answer=answer,
                    score=fb.get("score", 5),
                    strengths=fb.get("strengths", []),
                    improvements=fb.get("improvements", []),
                    ideal_answer_hints=fb.get("ideal_answer_hints", ""),
                )
            )

        overall_result = interview_graph.invoke(
            {
                "session_id": session_id,
                "task": "overall_feedback",
                "resume_text": session.resume_text,
                "jd_text": session.jd_text,
                "questions": interview.questions,
                "conversation_history": [
                    {"role": "user", "content": a} for a in interview.answers
                ],
                "messages": [],
            }
        )
        overall = overall_result.get("overall_feedback", {})

        roadmap_result = interview_graph.invoke(
            {
                "session_id": session_id,
                "task": "roadmap",
                "resume_text": session.resume_text,
                "jd_text": session.jd_text,
                "overall_feedback": overall,
                "questions": interview.questions,
                "conversation_history": [],
                "messages": [],
            }
        )
        raw_roadmap = roadmap_result.get("roadmap", [])

        roadmap = [
            RoadmapItem(
                topic=item.get("topic", ""),
                priority=item.get("priority", "Medium"),
                resources=item.get("resources", []),
                estimated_time=item.get("estimated_time", ""),
            )
            for item in raw_roadmap
        ]

        return FeedbackResponse(
            session_id=session_id,
            interview_id=interview_id,
            overall_score=overall.get("overall_score", 0),
            overall_summary=overall.get("overall_summary", ""),
            question_feedbacks=question_feedbacks,
            roadmap=roadmap,
            strengths=overall.get("strengths", []),
            areas_for_improvement=overall.get("areas_for_improvement", []),
        )
