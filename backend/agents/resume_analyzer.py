from agents.state import AgentState
from prompts import RESUME_ANALYSIS_PROMPT
from services.llm_service import generate


def resume_analyzer_node(state: AgentState) -> AgentState:
    prompt = RESUME_ANALYSIS_PROMPT.format(
        resume_text=state["resume_text"],
        jd_text=state.get("jd_text", "No JD provided."),
    )
    try:
        analysis = generate(prompt)
        return {**state, "analysis": analysis, "messages": ["Resume analysis complete."]}
    except Exception as e:
        return {**state, "error": str(e), "messages": [f"Resume analysis failed: {e}"]}
