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
            "skills": self.skill_extractor.extract_skills(),
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
        # Placeholder
        return []

    def extract_education(self):
        # Placeholder
        return []

    def extract_projects(self):
        # Placeholder
        return []