import re

class SkillExtractor:
    def __init__(self, skills_section_content):
        self.skills_section_content = skills_section_content

    def extract_skills(self):
        skills = {
            "technical": [],
            "frameworks": [],
            "tools": [],
            "languages": [],
            "soft": []
        }
        
        if self.skills_section_content:
            # This is a placeholder, we need to categorize skills
            skills["technical"] = [skill.strip() for skill in re.findall(r"- ([\w\s]+)", self.skills_section_content)]
            
        return skills
