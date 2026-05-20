import json
import re
from agents.state import AgentState
from prompts import ROADMAP_PROMPT
from services.llm_service import generate


def roadmap_agent_node(state: AgentState) -> AgentState:
    overall_feedback = state.get("overall_feedback", {})
    weak_areas = "\n".join(overall_feedback.get("areas_for_improvement", []))

    prompt = ROADMAP_PROMPT.format(
        resume_text=state.get("resume_text", "")[:1500],
        weak_areas=weak_areas or "General technical skills",
        jd_text=state.get("jd_text", "")[:1000],
    )
    try:
        roadmap = _parse_json_array(generate(prompt))
        return {**state, "roadmap": roadmap, "messages": ["Learning roadmap generated."]}
    except Exception as e:
        return {**state, "error": str(e), "messages": [f"Roadmap generation failed: {e}"]}


def _parse_json_array(text: str) -> list:
    text = text.strip()
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return json.loads(text)
