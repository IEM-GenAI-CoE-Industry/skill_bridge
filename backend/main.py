import os
import sys
import time
from dotenv import load_dotenv

# 1. PATH SETUP
# Ensure we can import from local folders (cv_analyzer, llm_workflows)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from langgraph.graph import StateGraph, END
from llm_workflows.gap_workflow import GapAnalysisState

# 2. IMPORT WORKFLOW NODES
try:
    # Node 1 & 2: Read & Extract
    from cv_analyzer.nlp_analyzer import cv_reader_node, extract_data_node
    
    # Node 3, 4 & 5: Requirements, Gap Analysis & PDF Report
    from cv_analyzer.gap_analysis_engine import (
        generate_job_requirements_node, 
        analyze_skill_gap_node, 
        generate_report_pdf_node
    )
    
    # Node 6: Skill Verification (Human-in-the-loop)
    from cv_analyzer.skill_verifier import skill_verification_node
    
    # Node 7: Final CV Generation
    from cv_analyzer.cv_generator import render_and_save_node

except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Ensure you are running this script from the 'backend' folder.")
    sys.exit(1)

# Load Environment Variables (API Keys)
load_dotenv()

def build_application():
    """
    Constructs the LangGraph State Machine.
    """
    print("🔧 Building Workflow Graph...")
    workflow = StateGraph(GapAnalysisState)

    # ADD NODES
    workflow.add_node("read_cv", cv_reader_node)
    workflow.add_node("extract_data", extract_data_node)
    workflow.add_node("gen_requirements", generate_job_requirements_node)
    workflow.add_node("analyze_gap", analyze_skill_gap_node)
    workflow.add_node("generate_gap_report", generate_report_pdf_node)
    workflow.add_node("verify_skills", skill_verification_node)
    workflow.add_node("generate_final_cv", render_and_save_node)

    # DEFINE EDGES (The Sequence)
    workflow.set_entry_point("read_cv")
    
    workflow.add_edge("read_cv", "extract_data")
    workflow.add_edge("extract_data", "gen_requirements")
    workflow.add_edge("gen_requirements", "analyze_gap")
    workflow.add_edge("analyze_gap", "generate_gap_report")
    workflow.add_edge("generate_gap_report", "verify_skills")
    workflow.add_edge("verify_skills", "generate_final_cv")
    workflow.add_edge("generate_final_cv", END)

    return workflow.compile()

def main():
    # Clear screen for a fresh start
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*60)
    print("🚀  FULL ORCHESTRATION")
    print("="*60)

    # 1. GET USER INPUTS
    while True:
        cv_path = input("\n📂 Enter path to your CV (PDF): ").strip().replace('"', '').replace("'", "")
        if os.path.exists(cv_path):
            break
        print("❌ File not found. Please try again.")

    job_title = input("💼 Enter the Target Job Title: ").strip()
    
    # Template Selection logic:
    # If user leaves it blank, we send "force_menu" to trigger the list in cv_generator.py
    template_input = input("🎨 Enter Template Number (1-3) [Press Enter to choose later]: ").strip()
    template_choice = template_input if template_input else "force_menu"

    print("\n" + "-"*60)
    print("⏳ Starting Pipeline...")
    print("-" * 60)

    # 2. INITIALIZE STATE
    initial_state = {
        "cv_file_path": cv_path,
        "job_title": job_title,
        "template_selection": template_choice
    }

    # 3. RUN WORKFLOW
    try:
        app = build_application()
        result = app.invoke(initial_state)

        # 4. FINAL SUMMARY
        print("\n" + "="*60)
        print("🎉  WORKFLOW COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        print(f"\n👤 Candidate: {result.get('user_name', 'Unknown')}")
        
        print("\n📄 OUTPUTS GENERATED:")
        if result.get('pdf_path'):
            print(f"   1. Skill Gap Report:   {result['pdf_path']}")
        
        if result.get('final_cv_path'):
            print(f"   2. Optimized CV:       {result['final_cv_path']}")
            
        print("\n✅ You can find these files in the 'backend/output' folder.")
        print("="*60)

    except Exception as e:
        error_msg = str(e)
        print("\n" + "!"*60)
        print("❌ WORKFLOW FAILED")
        print("!"*60)
        
        if "429" in error_msg or "Quota exceeded" in error_msg:
            print("\n⚠️  GOOGLE API QUOTA EXCEEDED")
            print("   You have hit the limit for the free tier.")
            print("   👉 ACTION: Wait 60 seconds and try again.")
        elif "404" in error_msg and "models/" in error_msg:
             print("\n⚠️  MODEL NAME ERROR")
             print("   The code is sending 'models/gemini-1.5-flash' but the API expects 'gemini-1.5-flash'.")
             print("   👉 ACTION: Check nlp_analyzer.py and remove the 'models/' prefix.")
        else:
            print(f"\nError Details: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()