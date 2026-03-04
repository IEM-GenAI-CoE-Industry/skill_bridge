# backend/cv_analyzer/skill_verifier.py

import os
import sys
import json
import google.generativeai as genai
from typing import List, Dict, Any
from dotenv import load_dotenv

# PATH SETUP
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from llm_workflows.gap_workflow import GapAnalysisState

# CONFIGURATION
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

MODEL_NAME = "gemini-2.5-flash"

# HELPER FUNCTIONS

def generate_questions(missing_skills: List[str]) -> List[Dict[str, Any]]:
    """
    Uses LLM to create simple Yes/No questions for the missing skills.
    """
    if not missing_skills:
        return []

    print(f"🧠 [Interviewer] Generating questions for {len(missing_skills)} skills...")

    prompt = f"""
    You are a Technical Recruiter. A candidate is missing these skills: {missing_skills}.
    Generate a very short, crisp question for each skill to check if they actually know it.
    The question format should strictly be: "Do you have experience with [Skill Name]?"
    
    Return a strict JSON list of objects matching this schema exactly:
    [ {{"skill": "Skill Name", "question": "...", "options": ["1. Yes", "2. No"]}} ]
    
    CRITICAL INSTRUCTION: Return ONLY the raw JSON object. No markdown.
    """
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"❌ Question Generation Error: {e}")
        return []

def verify_skills_with_user(questions: List[Dict[str, Any]]):
    """
    Interactive function: Asks user questions in the terminal.
    """
    skills_to_add = []
    skills_for_roadmap = [] 

    print("\n" + "="*50)
    print("🔍 SKILL CHECK (Requires Terminal Input)")
    print("="*50)
    
    for q in questions:
        print(f"🔹 {q['question']}")
        while True:
            choice = input("   👉 (1) Yes / (2) No: ").strip()
            if choice == "1":
                skills_to_add.append(q['skill'])
                break
            elif choice == "2":
                skills_for_roadmap.append(q['skill'])
                break
            else:
                print("   ⚠️ Invalid input. Enter 1 or 2.")

    return skills_to_add, skills_for_roadmap

# LANGGRAPH NODE

def skill_verification_node(state: GapAnalysisState) -> dict:
    """
    Node 6: Orchestrates skill verification with the user.
    Input: state['skill_report']['missing_skills']
    Updates: {'new_skills_to_add': [...], 'skills_for_roadmap': [...]}
    """
    # 1. Get missing skills directly from State (populated by Gap Engine)
    skill_report = state.get("skill_report", {})
    missing_skills = skill_report.get("missing_skills", [])
    
    if not missing_skills:
        print("✅ [Interviewer] No missing skills to verify. Skipping.")
        return {"new_skills_to_add": [], "skills_for_roadmap": []}
        
    # Limit to top 5 to keep the interview short
    top_missing_skills = missing_skills[:5]

    # 2. Generate Questions
    questions = generate_questions(top_missing_skills)
    
    if not questions:
        print("❌ Failed to generate questions. Skipping verification.")
        return {"new_skills_to_add": [], "skills_for_roadmap": []}

    # 3. Interactive Interview
    skills_to_add, skills_for_roadmap = verify_skills_with_user(questions)

    print(f"✅ Verified: Adding {len(skills_to_add)} skills to CV, {len(skills_for_roadmap)} to roadmap.")

    return {
        "new_skills_to_add": skills_to_add, 
        "skills_for_roadmap": skills_for_roadmap,
    }

# FULL INTEGRATION TEST BLOCK (NO MOCK DATA)
if __name__ == "__main__":
    from langgraph.graph import StateGraph, END
    
    # 1. Import Previous Nodes to Build Full Chain
    try:
        from cv_analyzer.nlp_analyzer import cv_reader_node, extract_data_node
        from cv_analyzer.gap_analysis_engine import generate_job_requirements_node, analyze_skill_gap_node
    except ImportError:
        # Handling path if running directly in folder
        sys.path.append(os.path.join(BASE_DIR, 'cv_analyzer'))
        from nlp_analyzer import cv_reader_node, extract_data_node
        from gap_analysis_engine import generate_job_requirements_node, analyze_skill_gap_node

    print("\n" + "="*50)
    print("🔗 SKILL VERIFICATION: FULL WORKFLOW TEST")
    print("="*50)

    # 2. Build the Full Graph
    workflow = StateGraph(GapAnalysisState)
    
    # Add Nodes
    workflow.add_node("read_cv", cv_reader_node)
    workflow.add_node("extract_data", extract_data_node)
    workflow.add_node("gen_requirements", generate_job_requirements_node)
    workflow.add_node("analyze_gap", analyze_skill_gap_node)
    workflow.add_node("verify_skills", skill_verification_node) # <-- The new node
    
    # Connect Edges
    workflow.set_entry_point("read_cv")
    workflow.add_edge("read_cv", "extract_data")
    workflow.add_edge("extract_data", "gen_requirements")
    workflow.add_edge("gen_requirements", "analyze_gap")
    workflow.add_edge("analyze_gap", "verify_skills")
    workflow.add_edge("verify_skills", END)
    
    app = workflow.compile()
    
    # 3. Get Real User Input
    while True:
        cv_path = input("\n📂 Enter Real CV Path: ").strip().replace('"', '').replace("'", "")
        if os.path.exists(cv_path): break
        print("❌ File not found.")
        
    job_title = input("💼 Enter Target Job Title: ").strip()
    
    inputs = {
        "cv_file_path": cv_path,
        "job_title": job_title
    }
    
    print(f"\n🚀 Running full analysis & verification...")
    
    try:
        result = app.invoke(inputs)
        
        print("\n" + "-"*30)
        print("🎉 PROCESS COMPLETE")
        print(f"✅ Skills added to CV: {result.get('new_skills_to_add')}")
        print(f"📚 Skills sent to Roadmap: {result.get('skills_for_roadmap')}")
        print("-" * 30)
        
    except Exception as e:
        print(f"\n❌ Pipeline Failed: {e}")