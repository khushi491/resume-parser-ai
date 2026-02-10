import re

class SkillExtractor:
    def __init__(self, text):
        self.text = text

    def extract_skills(self):
        # This is a very basic skill extractor, it can be improved a lot
        skills = {
            "technical": [],
            "frameworks": [],
            "tools": [],
            "languages": [],
            "soft": []
        }
        
        # Simple regex to find skills under a "Skills" section
        match = re.search(r"Skills\n(.*?)\n\n", self.text, re.DOTALL)
        if match:
            skills_text = match.group(1)
            # This is a placeholder, we need to categorize skills
            skills["technical"] = [skill.strip() for skill in re.findall(r"- ([\w\s]+)", skills_text)]
            
        return skills
