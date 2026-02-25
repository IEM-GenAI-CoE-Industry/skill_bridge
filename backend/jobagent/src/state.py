from typing import TypedDict, List, Dict


class AgentState(TypedDict):
    role: str
    location: str
    raw_results: List[Dict]
    filtered_jobs: List[Dict]
