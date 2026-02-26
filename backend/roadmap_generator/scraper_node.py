import os
from pypdf import PdfReader
from roadmap_mvp_state import RoadmapState

def scraper_node(state: RoadmapState) -> RoadmapState:
    """Reads the Skill_Report.pdf and saves text to state."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Assuming Skill_Report.pdf is in the same folder as this script
    report_path = os.path.join(current_dir, "Skill_Report.pdf")
    
    print(f"📄 Node 1 (Scraper): Reading {report_path}...")
    
    extracted_text = ""
    try:
        if os.path.exists(report_path):
            reader = PdfReader(report_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
            print("✅ Scraper: Text extracted successfully.")
        else:
            print(f"❌ Scraper Error: File not found at {report_path}")
            
    except Exception as e:
        print(f"❌ Scraper Error: {e}")

    # Return only the keys you want to update in the state
    return {"report_content": extracted_text}