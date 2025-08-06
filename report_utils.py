# report_utils.py
import os
import json
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

def save_report_as_pdf(session_id, content, output_dir="research_sessions"):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{session_id}.pdf")
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [Paragraph("Research Summary", styles["Heading1"]), Spacer(1, 12)]

    for block in content.split("\n"):
        elements.append(Paragraph(block.strip(), styles["BodyText"]))
        elements.append(Spacer(1, 6))

    doc.build(elements)
    return filename

def save_session_to_disk(session_id, topic, steps, output_dir="research_sessions"):
    os.makedirs(output_dir, exist_ok=True)
    session_data = {
        "session_id": session_id,
        "topic": topic,
        "steps": steps,
        "timestamp": datetime.now().isoformat()
    }
    path = os.path.join(output_dir, f"{session_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, indent=2)
    return path

def save_pdf_report(report_text, file_path="report.pdf"):
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    story = [Paragraph(report_text.replace("\n", "<br />"), styles["Normal"])]
    doc.build(story)


def save_markdown_report(report_text, file_path="report.md"):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report_text)