from .scraper import fetch_job_data
from .agent_core import find_matching_jobs
from .state import AgentState


def search_jobs_node(state: AgentState):
    print(f"--- Action: Searching for {state['role']} in {state['location']} ---")
    results = fetch_job_data(state["role"], state["location"])
    return {"raw_results": results}


def filter_jobs_node(state: AgentState):
    print("--- Action: Filtering matches ---")
    matches = find_matching_jobs(state["raw_results"], state["role"])
    return {"filtered_jobs": matches}
