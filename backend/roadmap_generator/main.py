import json
from langgraph.graph import StateGraph, END
from roadmap_mvp_state import RoadmapState
from scraper_node import scraper_node
from generator_node import generator_node

def run_app():
    # 1. Initialize Graph with State Schema
    builder = StateGraph(RoadmapState)

    # 2. Add Nodes
    builder.add_node("extract_text", scraper_node)
    builder.add_node("generate_roadmap", generator_node)

    # 3. Define Flow (Edges)
    builder.set_entry_point("extract_text")
    builder.add_edge("extract_text", "generate_roadmap")
    builder.add_edge("generate_roadmap", END)

    # 4. Compile
    graph = builder.compile()

    # 5. Execute
    print("🚀 Starting Career Coach Workflow...")
    initial_state = {
        "report_content": "",
        "skills_to_learn": [],
        "final_roadmap_json": {}
    }
    
    final_state = graph.invoke(initial_state)

    # 6. Output Result
    print("\n--- FINAL ROADMAP ---")
    print(json.dumps(final_state["final_roadmap_json"], indent=4))

if __name__ == "__main__":
    run_app()