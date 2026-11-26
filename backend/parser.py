import re
import pymupdf
from docx import Document


def read_resume(path, extension):
    if extension == ".pdf":
        doc = pymupdf.open(path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
    else:
        doc = Document(path)
        text = "\n".join(p.text for p in doc.paragraphs)
    return text.strip()


def estimate_years(text):
    t = text.lower()
    years = [int(m) for m in re.findall(r"(\d{1,2})\+?\s*(?:years|yrs)", t)]
    if years:
        return float(max(years))
    if "intern" in t:
        return 0.5
    return 0.0
