import re
import spacy

# Load a pre-trained spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class SkillExtractor:
    def __init__(self, skills_section_content):
        self.skills_section_content = skills_section_content
        # Define keywords for categorization (can be expanded)
        self.technical_keywords = ["python", "java", "c++", "c#", "javascript", "typescript", "golang", "ruby", "php", "swift", "kotlin", "html", "css", "sql", "nosql", "bash", "shell", "r", "matlab", "scala", "go", "rust"]
        self.framework_keywords = ["react", "angular", "vue", "django", "flask", "spring", "spring boot", "node.js", "express.js", "ruby on rails", "asp.net", "laravel", "symfony", "tensorflow", "pytorch", "keras", "scikit-learn", "numpy", "pandas"]
        self.tool_keywords = ["docker", "kubernetes", "aws", "azure", "gcp", "git", "jenkins", "jira", "confluence", "trello", "webpack", "babel", "maven", "gradle", "terraform", "ansible", "kubernetes", "vscode", "intellij", "pycharm", "jira"]
        self.language_keywords = ["english", "spanish", "french", "german", "mandarin", "japanese"]
        self.soft_skill_keywords = ["communication", "teamwork", "leadership", "problem-solving", "adaptability", "creativity", "time management", "critical thinking", "interpersonal", "collaboration", "client management", "project management"]


    def extract_skills(self):
        skills = {
            "technical": [],
            "frameworks": [],
            "tools": [],
            "languages": [],
            "soft": []
        }
        
        if not self.skills_section_content:
            return skills

        # Pre-process content: split by lines, strip whitespace, remove leading hyphens
        cleaned_lines = []
        for line in self.skills_section_content.split('\n'):
            stripped_line = line.strip()
            if stripped_line.startswith('-'):
                stripped_line = stripped_line[1:].strip() # Remove hyphen and re-strip
            if stripped_line:
                cleaned_lines.append(stripped_line)
        
        preprocessed_content = ", ".join(cleaned_lines) # Join back for consistent splitting

        doc = nlp(preprocessed_content.lower()) # Process the skills section content

        # Split by comma or newline for now, to keep "Problem-Solving" together
        potential_skills = re.split(r'[,\n]', preprocessed_content)
        extracted_skill_phrases = [skill.strip() for skill in potential_skills if skill.strip()]

        for skill_phrase in extracted_skill_phrases:
            skill_phrase_lower = skill_phrase.lower()
            
            categorized = False

            # Check for exact matches or strong inclusions
            # Prioritize soft skills, then specific technical categories
            if any(kw == skill_phrase_lower for kw in self.soft_skill_keywords): # Exact match for soft skills
                skills["soft"].append(skill_phrase)
                categorized = True
            elif any(kw in skill_phrase_lower for kw in self.framework_keywords):
                skills["frameworks"].append(skill_phrase)
                categorized = True
            elif any(kw in skill_phrase_lower for kw in self.tool_keywords):
                skills["tools"].append(skill_phrase)
                categorized = True
            elif any(kw in skill_phrase_lower for kw in self.technical_keywords):
                skills["technical"].append(skill_phrase)
                categorized = True
            elif any(kw in skill_phrase_lower for kw in self.language_keywords): # Languages typically less common in skills section
                skills["languages"].append(skill_phrase)
                categorized = True
            
            # If not categorized by specific keywords, add to technical as a general bucket
            if not categorized and skill_phrase:
                 # Avoid adding very short or generic words that are not skills
                if len(skill_phrase) > 2 and "and" not in skill_phrase_lower and "or" not in skill_phrase_lower:
                    skills["technical"].append(skill_phrase)
            
            # Remove duplicates and clean up lists
            ACRONYMS = ["AWS", "GCP", "SQL", "HTML", "CSS", "API", "C++", "C#"]
            for category in skills:
                cleaned_skills = []
                for s in skills[category]:
                    if s.upper() in ACRONYMS:
                        cleaned_skills.append(s.upper()) # Keep acronyms uppercase
                    else:
                        cleaned_skills.append(s.title()) # Capitalize other skills
                skills[category] = list(set(cleaned_skills))
        
        return skills
