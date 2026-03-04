from pypdf import PdfReader
from .roadmap_mvp_state import RoadmapState


def scraper_node(state: RoadmapState) -> RoadmapState:
    """
    Extract text from Skill_Report.pdf and store in state["report_content"]
    """

    try:
        pdf_path = "roadmap_generator/Skill_Report.pdf"
        reader = PdfReader(pdf_path)

        extracted_text = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

        return {
            **state,
            "report_content": extracted_text
        }

    except Exception as e:
        return {
            **state,
            "report_content": f"Error: {str(e)}"
        }