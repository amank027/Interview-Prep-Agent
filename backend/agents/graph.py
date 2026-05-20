from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.resume_analyzer import resume_analyzer_node
from agents.question_generator import question_generator_node
from agents.mock_interview import mock_interview_node
from agents.feedback_agent import feedback_agent_node, overall_feedback_node
from agents.roadmap_agent import roadmap_agent_node


def _route_task(state: AgentState) -> str:
    task = state.get("task", "")
    routing = {
        "analyze_resume": "resume_analyzer",
        "generate_questions": "question_generator",
        "mock_interview": "mock_interview",
        "feedback": "feedback_agent",
        "overall_feedback": "overall_feedback_agent",
        "roadmap": "roadmap_agent",
    }
    return routing.get(task, END)


def build_interview_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("resume_analyzer", resume_analyzer_node)
    graph.add_node("question_generator", question_generator_node)
    graph.add_node("mock_interview", mock_interview_node)
    graph.add_node("feedback_agent", feedback_agent_node)
    graph.add_node("overall_feedback_agent", overall_feedback_node)
    graph.add_node("roadmap_agent", roadmap_agent_node)

    graph.set_conditional_entry_point(
        _route_task,
        {
            "resume_analyzer": "resume_analyzer",
            "question_generator": "question_generator",
            "mock_interview": "mock_interview",
            "feedback_agent": "feedback_agent",
            "overall_feedback_agent": "overall_feedback_agent",
            "roadmap_agent": "roadmap_agent",
            END: END,
        },
    )

    for node in [
        "resume_analyzer",
        "question_generator",
        "mock_interview",
        "feedback_agent",
        "overall_feedback_agent",
        "roadmap_agent",
    ]:
        graph.add_edge(node, END)

    return graph.compile()


# Singleton compiled graph
interview_graph = build_interview_graph()
