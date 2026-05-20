from fastapi import APIRouter, Depends
from models import (
    StartInterviewRequest,
    StartInterviewResponse,
    AnswerRequest,
    AnswerResponse,
)
from controllers import InterviewController
from services import SessionService
from core.dependencies import get_session_service

router = APIRouter(prefix="/interview", tags=["Interview"])


def _get_interview_controller(
    session_svc: SessionService = Depends(get_session_service),
) -> InterviewController:
    return InterviewController(session_svc)


@router.post("/start", response_model=StartInterviewResponse)
def start_interview(
    request: StartInterviewRequest,
    controller: InterviewController = Depends(_get_interview_controller),
) -> StartInterviewResponse:
    return controller.start_interview(request)


@router.post("/answer", response_model=AnswerResponse)
def submit_answer(
    request: AnswerRequest,
    controller: InterviewController = Depends(_get_interview_controller),
) -> AnswerResponse:
    return controller.submit_answer(request)
