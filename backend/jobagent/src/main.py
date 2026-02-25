from .graph import create_job_agent
from .config import DEFAULT_LOCATION


def display_results(jobs):
    if not jobs:
        print("\n--- No Matching Jobs Found ---")
        return

    print(f"\n--- Found {len(jobs)} Matching Job Openings ---")
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   URL: {job['url']}")


def run_agent():
    print("=== Job Matching Agent ===")

    # 1. Gather User Input
    role = input("Enter the job role (e.g., Frontend Developer): ").strip()
    if not role:
        print("Role is required.")
        return

    loc_input = input(f"Enter location (Default: {DEFAULT_LOCATION}): ").strip()
    location = loc_input if loc_input else DEFAULT_LOCATION

    # 2. Initialize the Compiled Graph
    app = create_job_agent()

    # 3. Define the Initial State
    # This must match the keys defined in your AgentState TypedDict
    initial_state = {
        "role": role,
        "location": location,
        "raw_results": [],
        "filtered_jobs": [],
    }

    # 4. Invoke the Graph
    print(f"\n[Agent]: Starting workflow for {role} in {location}...")
    try:
        # The graph will run 'searcher' then 'filterer' automatically
        final_state = app.invoke(initial_state)

        # 5. Extract results from the final state
        display_results(final_state.get("filtered_jobs", []))

    except Exception as e:
        print(f"An error occurred during graph execution: {e}")


if __name__ == "__main__":
    # Run as: python -m src.main
    run_agent()
