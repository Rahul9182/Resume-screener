import uuid
import re

def generate_resume_id():
    return str(uuid.uuid4())

def clean_text(text):
    text = text.replace('\r', ' ').replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_section(text, section, next_sections=None):
    """
    Extracts a section by header name. If regex fails due to an extension error (bad input), logs and returns ''.
    """
    def safe_section(s):
        if not s or not isinstance(s, str):
            print(f"[WARN] Skipping invalid section header: {s}")
            return False
        # Forbid deeply weird characters
        if not re.match(r'^[\w \-\.:/]+$', s, re.UNICODE):
            print(f"[WARN] Skipping unsafe section header (not matched): {s}")
            return False
        # Don't allow totally numeric or super short
        if len(s.strip()) < 2 or s.strip().isdigit():
            print(f"[WARN] Skipping trivial section header: {s}")
            return False
        return True
    if not next_sections:
        # Most common section boundaries
        next_sections = [
            'Education', 'Experience', 'Skills', 'Projects', 'Certifications', 'Summary', 'Objective', 'Personal', 'Achievements', 'Contact', 'References'
        ]
    safe_headers = [h for h in next_sections if safe_section(h)]
    if not safe_headers:
        print("[WARN] No safe section headers for alternation!")
        safe_headers = ['Education', 'Experience']
    alternation = '|'.join(re.escape(h) for h in safe_headers)
    safe_sec = section.strip() if safe_section(section) else ''
    if not safe_sec:
        print(f"[WARN] extract_section called with unsafe section: {section}")
        return ''
    section_rgx = rf'(^|\n|\r)[\s\-\:]*{re.escape(safe_sec)}[\s\-\:]*[\n\r]+(.*?)(?=^({alternation})[\s\-\:]?[\n\r]|\Z)'
    try:
        matches = re.findall(section_rgx, text, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        if matches:
            return matches[0][1].strip()
        return ''
    except Exception as e:
        # Print all details so user can debug broken PDFs
        print(f"[ERROR] extract_section regex failed: {e}. Section: '{section}', Pattern: '{section_rgx}' Alternation: '{alternation}'")
        return ''

def split_into_sections(text):
    headers = [
        'education', 'experience', 'skills', 'certifications', 'summary', 'objective', 'personal', 'achievements', 'contact', 'references'
    ]
    result = {}
    for idx, section in enumerate(headers):
        sec_clean = section.lower().strip()
        result[sec_clean] = extract_section(text, sec_clean, next_sections=[h.lower().strip() for h in headers[idx+1:]])
    return result