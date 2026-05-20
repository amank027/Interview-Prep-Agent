import re
from agents.state import AgentState
from prompts import QUESTION_GENERATION_PROMPT
from services.llm_service import generate


def question_generator_node(state: AgentState) -> AgentState:
    num_questions = state.get("num_questions", 5)
    interview_type = state.get("interview_type", "technical")

    prompt = QUESTION_GENERATION_PROMPT.format(
        num_questions=num_questions,
        interview_type=interview_type,
        resume_text=state.get("resume_text", ""),
        jd_text=state.get("jd_text", ""),
    )
    try:
        text = generate(prompt)
        questions = _parse_questions(text, num_questions)
        return {**state, "questions": questions, "messages": [f"Generated {len(questions)} questions."]}
    except Exception as e:
        return {**state, "error": str(e), "messages": [f"Question generation failed: {e}"]}


def _parse_questions(text: str, expected: int) -> list[str]:
    lines = text.strip().split("\n")
    questions = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        cleaned = re.sub(r"^\d+[\.\)]\s*", "", line).strip()
        if cleaned and len(cleaned) > 10:
            questions.append(cleaned)
    return questions[:expected] if questions else [text.strip()]
