import os
import re
from typing import Optional, Dict
from pydantic import BaseModel, Field

try:
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.output_parsers import PydanticOutputParser
except Exception:
    ChatOpenAI = None  # type: ignore
    ChatPromptTemplate = None  # type: ignore
    PydanticOutputParser = None  # type: ignore

class ResumeFields(BaseModel):
    name: str = Field(default='Not Found')
    email: str = Field(default='Not Found')
    phone: str = Field(default='Not Found')
    linkedin: str = Field(default='Not Found')
    github: str = Field(default='Not Found')

    highest_degree: str = Field(default='Not Found')
    college_name: str = Field(default='Not Found')
    graduation_year: str = Field(default='Not Found')
    major: str = Field(default='Not Found')
    cgpa: str = Field(default='Not Found')

    total_experience_years: float = Field(default=0.0)
    current_company: str = Field(default='Not Found')
    current_designation: str = Field(default='Not Found')
    previous_companies: str = Field(default='Not Found')

    technical_skills: str = Field(default='Not Found')
    programming_languages: str = Field(default='Not Found')
    frameworks_tools: str = Field(default='Not Found')
    soft_skills: str = Field(default='Not Found')
    certifications: str = Field(default='Not Found')

SYSTEM_PROMPT = (
    "You are a highly reliable resume parser. Return only the requested structured data."
    " If information is missing, use 'Not Found'. For experience years, return a number."
)

USER_PROMPT = (
    "Extract the fields from the resume text below. Be precise and avoid hallucinations.\n\n"
    "Resume Text:\n{resume_text}"
)

def extract_with_langchain(resume_text: str) -> dict:
    if not resume_text or len(resume_text.strip()) < 20:
        return {}
    if ChatOpenAI is None:
        # LangChain not available, fallback to rules
        return extract_with_rules(resume_text)
    try:
        parser = PydanticOutputParser(pydantic_object=ResumeFields)
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", USER_PROMPT + "\n\n{format_instructions}")
        ])
        chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0.0) | parser
        result: ResumeFields = chain.invoke({
            "resume_text": resume_text[:12000],
            "format_instructions": parser.get_format_instructions()
        })
        data = result.model_dump()
        # If model returns empty/mostly defaults, try rules as a backup enhancer
        if not data or all(v in ("Not Found", 0.0, "") for v in data.values()):
            rule_data = extract_with_rules(resume_text)
            # Merge rule-based extracted values into data where empty
            for k, v in rule_data.items():
                if k in data and (data[k] in ("Not Found", 0.0, "") or not data[k]):
                    data[k] = v
        return data
    except Exception as e:
        print(f"[WARN] LangChain extraction failed: {e}")
        # Fallback to rules
        return extract_with_rules(resume_text)


def extract_with_rules(resume_text: str) -> Dict[str, any]:
    """
    Lightweight rule-based extractor used as a fallback when LLM isn't available.
    """
    text = resume_text or ""
    data: Dict[str, any] = {
        'name': 'Not Found',
        'email': 'Not Found',
        'phone': 'Not Found',
        'linkedin': 'Not Found',
        'github': 'Not Found',
        'highest_degree': 'Not Found',
        'college_name': 'Not Found',
        'graduation_year': 'Not Found',
        'major': 'Not Found',
        'cgpa': 'Not Found',
        'total_experience_years': 0.0,
        'current_company': 'Not Found',
        'current_designation': 'Not Found',
        'previous_companies': 'Not Found',
        'technical_skills': 'Not Found',
        'programming_languages': 'Not Found',
        'frameworks_tools': 'Not Found',
        'soft_skills': 'Not Found',
        'certifications': 'Not Found',
    }

    # Email
    m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if m:
        data['email'] = m.group(0)

    # Phone
    m = re.search(r"(?:(?:\+?\d{1,3}[\s.-]?)?(?:\(\d{2,4}\)[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}[\s.-]?\d{0,4})", text)
    if m and len(m.group(0).strip()) >= 10:
        data['phone'] = m.group(0).strip()

    # LinkedIn / GitHub
    m = re.search(r"linkedin\.com\S*", text, re.IGNORECASE)
    if m:
        data['linkedin'] = m.group(0)
    m = re.search(r"github\.com\S*", text, re.IGNORECASE)
    if m:
        data['github'] = m.group(0)

    # Name heuristic: first non-empty line that is not a header keyword
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    header_keywords = {"objective", "summary", "experience", "education", "skills"}
    for ln in lines[:10]:
        if len(ln.split()) <= 6 and ln.lower() not in header_keywords and not re.search(r"@|linkedin|github|\d", ln, re.I):
            data['name'] = ln
            break

    # Degree and graduation year
    degree_map = {
        'phd': 'PhD', 'doctor': 'PhD', 'masters': 'Masters', 'ms': 'Masters', 'm.s': 'Masters',
        'm.tech': 'Masters', 'mtech': 'Masters', 'bachelors': 'Bachelors', 'bs': 'Bachelors', 'b.s': 'Bachelors',
        'b.tech': 'Bachelors', 'btech': 'Bachelors'
    }
    lowered = text.lower()
    for key, val in degree_map.items():
        if key in lowered:
            data['highest_degree'] = val
            break
    m = re.search(r"(19|20)\d{2}", text)
    if m:
        data['graduation_year'] = m.group(0)

    # Technical skills section
    skills_section = None
    for i, ln in enumerate(lines):
        if re.match(r"^skills\b", ln, re.I):
            # take next up to 10 lines as skills context
            skills_section = " ".join(lines[i:i+10])
            break
    if skills_section:
        # split by separators
        parts = re.split(r"[,\|\n;]", skills_section)
        tokens = sorted(set([p.strip() for p in parts if len(p.strip()) >= 2]))
        if tokens:
            data['technical_skills'] = ", ".join(tokens)

    return data
