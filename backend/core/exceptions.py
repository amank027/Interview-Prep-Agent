from fastapi import HTTPException, status


class SessionNotFoundError(HTTPException):
    def __init__(self, session_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session '{session_id}' not found.",
        )


class InterviewNotFoundError(HTTPException):
    def __init__(self, interview_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Interview '{interview_id}' not found.",
        )


class DocumentNotUploadedError(HTTPException):
    def __init__(self, doc_type: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No {doc_type} uploaded for this session. Please upload first.",
        )


class UnsupportedFileTypeError(HTTPException):
    def __init__(self, filename: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"File '{filename}' is not supported. Only PDF and TXT files are accepted.",
        )


class InterviewAlreadyCompleteError(HTTPException):
    def __init__(self, interview_id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Interview '{interview_id}' is already complete.",
        )
