import re
import docx
import spacy
from pdfminer.high_level import extract_text

nlp = spacy.load("en_core_web_sm")

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_pdf(file_path):
    return extract_text(file_path)

def extract_info_from_resume(file_path):
    text = extract_text_from_docx(file_path) if file_path.endswith(".docx") else extract_text(file_path)
    info = {
        "Name": "",
        "Email": "",
        "Phone": "",
        "Experience": "",
        "Skills": ""
    }

    email_match = re.search(r'\S+@\S+', text)
    if email_match:
        info["Email"] = email_match.group(0)

    phone_match = re.search(r'(\+91[-\s]?)?\d{10}', text)
    if phone_match:
        info["Phone"] = phone_match.group(0)

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            info["Name"] = ent.text
            break

    exp_match = re.search(r'(\d+)\+?\s+(years|yrs?)\s+(of)?\s*experience', text, re.I)
    if exp_match:
        info["Experience"] = exp_match.group(1) + " years"

    skills = ['Python', 'Java', 'SQL', 'AWS', 'Machine Learning', 'Excel', 'C++']
    info["Skills"] = ', '.join([s for s in skills if s.lower() in text.lower()])

    return info