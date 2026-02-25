from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import search_jobs_node, filter_jobs_node


def create_job_agent():
    # Initialize the graph with the State schema
    workflow = StateGraph(AgentState)

    # Define the nodes
    workflow.add_node("searcher", search_jobs_node)
    workflow.add_node("filterer", filter_jobs_node)

    # Define the edges (the flow)
    workflow.set_entry_point("searcher")
    workflow.add_edge("searcher", "filterer")
    workflow.add_edge("filterer", END)

    return workflow.compile()
