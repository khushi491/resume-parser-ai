import re
import json
from parser.skill_extractor import SkillExtractor
from parser.utils import split_into_sections

class ResumeParser:
    def __init__(self, resume_text):
        self.resume_text = resume_text
        self.sections = split_into_sections(resume_text)
        self.skill_extractor = None

    def parse(self):
        personal_info = self.extract_personal_info()
        return {
            "personal_info": personal_info,
            "summary": self.extract_summary(),
            "skills": self.extract_skills(), # This line will be changed in the next commit
            "experience": self.extract_experience(),
            "education": self.extract_education(),
            "projects": self.extract_projects(),
            "certifications": [],
            "total_experience_years": 0,
            "confidence_score": 0,
            "missing_fields": []
        }

    def extract_personal_info(self):
        name = self.extract_name()
        email = self.extract_email()
        phone = self.extract_phone()
        location = self.extract_location()
        linkedin = self.extract_linkedin()
        github = self.extract_github()
        portfolio = self.extract_portfolio()

        return {
            "full_name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "linkedin": linkedin,
            "github": github,
            "portfolio": portfolio
        }

    def extract_name(self):
        # This is a simple regex, a more robust solution would be to use NLP
        text = self.resume_text.strip()
        match = re.search(r"([A-Z][a-z]+(?: [A-Z][a-z]+)+)", text)
        return match.group(0) if match else None

    def extract_email(self):
        match = re.search(r"[\w\.-]+@[\w\.-]+", self.resume_text)
        return match.group(0) if match else None

    def extract_phone(self):
        match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", self.resume_text)
        return match.group(0) if match else None

    def extract_location(self):
        # This is a very basic regex and will need to be improved
        match = re.search(r"((?:[A-Z][a-z]+(?: )?)+, [A-Z]{2})", self.resume_text)
        return match.group(0) if match else None

    def extract_linkedin(self):
        match = re.search(r"linkedin\.com/in/[\w-]+", self.resume_text)
        return match.group(0) if match else None

    def extract_github(self):
        match = re.search(r"github\.com/[\w-]+", self.resume_text)
        return match.group(0) if match else None

    def extract_portfolio(self):
        # Look for a URL that is not linkedin or github
        match = re.search(r"(https?://[^\s/$.?#].[^\s]*)", self.resume_text)
        if match:
            url = match.group(0)
            if "linkedin.com" not in url and "github.com" not in url:
                return url
        return None

    def extract_summary(self):
        # Find the "Summary" section in the pre-processed sections
        for title, content in self.sections.items():
            if title.lower() == "summary":
                return content.strip()
        return None

    def extract_skills(self):
        skills_section_content = ""
        for title, content in self.sections.items():
            if title.lower() == "skills":
                skills_section_content = content
                break
        
        self.skill_extractor = SkillExtractor(skills_section_content)
        return self.skill_extractor.extract_skills()

    def extract_experience(self):
        experience_section_content = ""
        for title, content in self.sections.items():
            if title.lower() == "experience":
                experience_section_content = content
                break

        experiences = []
        if not experience_section_content:
            return experiences

        # Split into individual job entries more robustly
        # Look for lines that start with a potential job title or company name.
        # This is a heuristic and might need refinement for various resume formats.
        lines = experience_section_content.split('\n')
        job_entries_raw = []
        current_job_entry = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Heuristic: A new job entry often starts with a line containing
            # a role (e.g., Software Engineer) or a company name (e.g., Acme Inc.)
            # and often includes a date or date range on the same or next line.
            # For simplicity, let's assume a new job entry starts with a line
            # that is not a bullet point description.
            # Or, a line that contains " at " or " | " which often separates role and company.
            if (re.search(r'\b(?:Engineer|Developer|Manager|Analyst)\b', line, re.IGNORECASE) or
                re.search(r'\b(?:Inc\.|Corp\.|LLC|Ltd\.)\b', line) or
                re.search(r'^\S+(?: at |\s*\|\s*)\S+', line)): # Starts with something then ' at ' or ' | '
                if current_job_entry:
                    job_entries_raw.append("\n".join(current_job_entry))
                current_job_entry = [line]
            else:
                current_job_entry.append(line)
        
        if current_job_entry:
            job_entries_raw.append("\n".join(current_job_entry))

        for entry_text in job_entries_raw:
            job_details = self._parse_job_entry(entry_text)
            if job_details:
                experiences.append(job_details)
        
        return experiences

    def _parse_job_entry(self, entry_text):
        company = None
        role = None
        location = None
        start_date = None
        end_date = None
        is_current = False
        description = []
        technologies = []

        lines = entry_text.split('\n')
        header_lines = []
        description_lines = []

        # Separate header lines from description lines (usually bullet points)
        for line in lines:
            if line.strip().startswith('-'):
                description_lines.append(line.strip())
            else:
                header_lines.append(line.strip())

        header = " ".join(header_lines)

        # Extract Role and Company
        # Pattern: Role at Company | Location | Dates
        # Pattern: Company | Role | Location | Dates
        role_company_match = re.search(r"^(.*?)(?: at | @ | in | \| )(.*?)(?: \| (.*?))?(?: \| (.*?))?$", header)
        if role_company_match:
            part1 = role_company_match.group(1).strip()
            part2 = role_company_match.group(2).strip()

            # Heuristics to determine role and company
            if re.search(r'\b(?:Engineer|Developer|Manager|Analyst)\b', part1, re.IGNORECASE) or 'Software' in part1:
                role = part1
                company = part2
            elif re.search(r'\b(?:Inc\.|Corp\.|LLC|Ltd\.)\b', part1):
                company = part1
                role = part2
            else: # Default: assume role then company
                role = part1
                company = part2
        else: # Try simpler approach if complex regex fails
            # Attempt to find role and company using common delimiters
            parts = [p.strip() for p in header.split('|') if p.strip()]
            if len(parts) >= 2:
                # Assuming the first two parts are likely role and company or vice versa
                if re.search(r'\b(?:Engineer|Developer|Manager|Analyst)\b', parts[0], re.IGNORECASE):
                    role = parts[0]
                    company = parts[1] if len(parts) > 1 else None
                elif re.search(r'\b(?:Inc\.|Corp\.|LLC|Ltd\.)\b', parts[0]):
                    company = parts[0]
                    role = parts[1] if len(parts) > 1 else None
                else: # Fallback
                    role = parts[0]
                    company = parts[1] if len(parts) > 1 else None
            elif len(parts) == 1:
                # If only one part, try to identify if it's a role or company
                if re.search(r'\b(?:Engineer|Developer|Manager|Analyst)\b', parts[0], re.IGNORECASE):
                    role = parts[0]
                else:
                    company = parts[0]


        # Extract Dates
        date_range_match = re.search(r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\s*-\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\s*\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\s*-\s*Present", header, re.IGNORECASE)
        if date_range_match:
            date_range = date_range_match.group(0)
            if 'Present' in date_range:
                is_current = True
                parts = date_range.split('-')
                start_date = parts[0].strip()
                end_date = None # As it's current
            else:
                parts = date_range.split('-')
                start_date = parts[0].strip()
                end_date = parts[1].strip()
        else: # Simpler date extraction
            # Try to find two four-digit years, possibly with months
            date_match_simple = re.findall(r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\s*(\d{4})", header, re.IGNORECASE)
            if len(date_match_simple) >= 2:
                start_date = date_match_simple[0]
                end_date = date_match_simple[1]
            elif len(date_match_simple) == 1 and 'Present' in header:
                start_date = date_match_simple[0]
                is_current = True


        # Extract Location
        # Look for patterns like "City, ST" or "City, Country"
        location_match = re.search(r"([A-Z][a-z]+(?: [A-Z][a-z]+)*, (?:[A-Z]{2}|\b\w+\b))", header)
        if location_match:
            location = location_match.group(0)

        # Technologies will be extracted later
        
        return {
            "company": company,
            "role": role,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "is_current": is_current,
            "description": "\n".join(description_lines),
            "technologies": technologies
        }

    def extract_education(self):
        # Placeholder
        return []

    def extract_projects(self):
        # Placeholder
        return []