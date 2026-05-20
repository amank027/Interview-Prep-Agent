from agents.state import AgentState


def mock_interview_node(state: AgentState) -> AgentState:
    questions = state.get("questions", [])
    history = state.get("conversation_history", [])
    current_answer = state.get("user_answer", "")

    if current_answer:
        history = history + [{"role": "user", "content": current_answer}]

    answered_count = len([m for m in history if m["role"] == "user"])
    next_idx = answered_count

    if next_idx < len(questions):
        next_question = questions[next_idx]
        history = history + [{"role": "assistant", "content": next_question}]
        return {
            **state,
            "current_question": next_question,
            "conversation_history": history,
            "messages": [f"Presenting question {next_idx + 1}."],
        }
    else:
        return {
            **state,
            "current_question": "",
            "conversation_history": history,
            "messages": ["All questions answered."],
        }
