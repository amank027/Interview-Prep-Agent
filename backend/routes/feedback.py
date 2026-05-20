from fastapi import APIRouter, Depends
from models import FeedbackResponse
from controllers import FeedbackController
from services import SessionService
from core.dependencies import get_session_service

router = APIRouter(prefix="/feedback", tags=["Feedback"])


def _get_feedback_controller(
    session_svc: SessionService = Depends(get_session_service),
) -> FeedbackController:
    return FeedbackController(session_svc)


@router.get("/{session_id}/{interview_id}", response_model=FeedbackResponse)
def get_feedback(
    session_id: str,
    interview_id: str,
    controller: FeedbackController = Depends(_get_feedback_controller),
) -> FeedbackResponse:
    return controller.get_feedback(session_id, interview_id)
