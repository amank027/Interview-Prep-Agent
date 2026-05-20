import json
import re
from agents.state import AgentState
from prompts import FEEDBACK_PROMPT, OVERALL_FEEDBACK_PROMPT
from services.llm_service import generate


def feedback_agent_node(state: AgentState) -> AgentState:
    prompt = FEEDBACK_PROMPT.format(
        question=state.get("current_question", ""),
        answer=state.get("user_answer", ""),
        resume_context=state.get("resume_text", "")[:1000],
    )
    try:
        feedback = _parse_json(generate(prompt))
        return {**state, "feedback": feedback, "messages": ["Per-question feedback generated."]}
    except Exception as e:
        return {**state, "error": str(e), "messages": [f"Feedback generation failed: {e}"]}


def overall_feedback_node(state: AgentState) -> AgentState:
    questions = state.get("questions", [])
    history = state.get("conversation_history", [])
    user_answers = [m["content"] for m in history if m["role"] == "user"]

    qa_pairs = []
    for i, q in enumerate(questions):
        ans = user_answers[i] if i < len(user_answers) else "No answer provided"
        qa_pairs.append(f"Q{i+1}: {q}\nA: {ans}")

    prompt = OVERALL_FEEDBACK_PROMPT.format(
        qa_summary="\n\n".join(qa_pairs),
        resume_text=state.get("resume_text", "")[:1500],
    )
    try:
        overall = _parse_json(generate(prompt))
        return {**state, "overall_feedback": overall, "messages": ["Overall feedback generated."]}
    except Exception as e:
        return {**state, "error": str(e), "messages": [f"Overall feedback failed: {e}"]}


def _parse_json(text: str) -> dict:
    text = text.strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return json.loads(text)
