from models import (
    StartInterviewRequest,
    StartInterviewResponse,
    AnswerRequest,
    AnswerResponse,
)
from services import SessionService
from agents import interview_graph
from core.exceptions import (
    DocumentNotUploadedError,
    InterviewNotFoundError,
    InterviewAlreadyCompleteError,
)


class InterviewController:
    def __init__(self, session_service: SessionService):
        self._session_svc = session_service

    def start_interview(self, request: StartInterviewRequest) -> StartInterviewResponse:
        session = self._session_svc.get_or_create(request.session_id)

        if not session.has_resume:
            raise DocumentNotUploadedError("resume")

        result = interview_graph.invoke(
            {
                "session_id": request.session_id,
                "task": "generate_questions",
                "resume_text": session.resume_text,
                "jd_text": session.jd_text,
                "interview_type": request.interview_type.value,
                "num_questions": request.num_questions,
                "conversation_history": [],
                "questions": [],
                "messages": [],
            }
        )

        questions = result.get("questions", [])
        if not questions:
            questions = ["Tell me about yourself and your technical background."]

        interview = self._session_svc.create_interview(
            session_id=request.session_id,
            interview_type=request.interview_type.value,
            questions=questions,
        )

        first_question = questions[0]
        interview.current_index = 0

        return StartInterviewResponse(
            session_id=request.session_id,
            interview_id=interview.interview_id,
            first_question=first_question,
            total_questions=len(questions),
            message="Interview started. Good luck!",
        )

    def submit_answer(self, request: AnswerRequest) -> AnswerResponse:
        interview = self._session_svc.get_interview(
            request.session_id, request.interview_id
        )
        if interview is None:
            raise InterviewNotFoundError(request.interview_id)

        if interview.is_complete:
            raise InterviewAlreadyCompleteError(request.interview_id)

        interview.answers.append(request.answer)
        interview.current_index += 1
        questions_answered = interview.current_index

        next_question: str | None = None
        is_complete = questions_answered >= len(interview.questions)

        if not is_complete:
            next_question = interview.questions[interview.current_index]
        else:
            interview.is_complete = True

        return AnswerResponse(
            session_id=request.session_id,
            interview_id=request.interview_id,
            next_question=next_question,
            is_complete=is_complete,
            questions_answered=questions_answered,
            total_questions=len(interview.questions),
            message="Answer recorded." if not is_complete else "Interview complete! Fetch your feedback.",
        )
