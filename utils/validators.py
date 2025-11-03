import re

# Data validation

def validate_resume_data(data):
    keys = [
        'resume_id', 'file_name', 'upload_date', 'name', 'email', 'phone',
        'highest_degree', 'college_name', 'graduation_year', 'major', 'cgpa',
        'total_experience_years', 'current_company', 'current_designation', 'previous_companies',
        'technical_skills', 'programming_languages', 'frameworks_tools', 'soft_skills', 'certifications', 'linkedin', 'github'
    ]
    clean = {}
    for k in keys:
        v = data.get(k, 'Not Found')
        if k == 'total_experience_years':
            try:
                # Accept numeric, numeric-like strings; else default 0.0
                if isinstance(v, (int, float)):
                    clean[k] = float(v)
                else:
                    # Extract first float-like number if present
                    num = re.findall(r"\d+(?:\.\d+)?", str(v))
                    clean[k] = float(num[0]) if num else 0.0
                continue
            except Exception:
                clean[k] = 0.0
                continue
        if k == 'graduation_year':
            try:
                # Extract a 4-digit year if present, else empty string for Arrow compatibility
                year_match = re.search(r"(19|20)\d{2}", str(v))
                v = year_match.group(0) if year_match else ''
            except Exception:
                v = ''
        if isinstance(v, str):
            v = v.strip()
        clean[k] = v
    return clean

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

def clean_phone_number(phone):
    return re.sub(r'[^+\d]', '', phone)