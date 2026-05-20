import uuid
from dataclasses import dataclass, field


@dataclass
class InterviewSession:
    interview_id: str
    session_id: str
    interview_type: str
    questions: list[str] = field(default_factory=list)
    answers: list[str] = field(default_factory=list)
    current_index: int = 0
    is_complete: bool = False


@dataclass
class UserSession:
    session_id: str
    has_resume: bool = False
    has_jd: bool = False
    resume_text: str = ""
    jd_text: str = ""
    conversation_history: list[dict] = field(default_factory=list)
    interviews: dict[str, InterviewSession] = field(default_factory=dict)


class SessionService:
    def __init__(self):
        self._sessions: dict[str, UserSession] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = UserSession(session_id=session_id)
        return session_id

    def get_session(self, session_id: str) -> UserSession | None:
        return self._sessions.get(session_id)

    def get_or_create(self, session_id: str) -> UserSession:
        if session_id not in self._sessions:
            self._sessions[session_id] = UserSession(session_id=session_id)
        return self._sessions[session_id]

    def update_document(
        self, session_id: str, doc_type: str, text: str
    ) -> None:
        session = self.get_or_create(session_id)
        if doc_type == "resume":
            session.has_resume = True
            session.resume_text = text
        elif doc_type == "jd":
            session.has_jd = True
            session.jd_text = text

    def create_interview(
        self,
        session_id: str,
        interview_type: str,
        questions: list[str],
    ) -> InterviewSession:
        session = self.get_or_create(session_id)
        interview_id = str(uuid.uuid4())
        interview = InterviewSession(
            interview_id=interview_id,
            session_id=session_id,
            interview_type=interview_type,
            questions=questions,
        )
        session.interviews[interview_id] = interview
        return interview

    def get_interview(
        self, session_id: str, interview_id: str
    ) -> InterviewSession | None:
        session = self.get_session(session_id)
        if session is None:
            return None
        return session.interviews.get(interview_id)

    def add_conversation_turn(
        self, session_id: str, role: str, content: str
    ) -> None:
        session = self.get_or_create(session_id)
        session.conversation_history.append({"role": role, "content": content})
