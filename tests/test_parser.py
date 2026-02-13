import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser.resume_parser import ResumeParser

class TestResumeParser(unittest.TestCase):

    def setUp(self):
        self.resume_text = """
John Doe
New York, NY | 123-456-7890 | john.doe@example.com | linkedin.com/in/johndoe | github.com/johndoe

Summary
A highly motivated software engineer with 5 years of experience.

Skills
- Python, Java, C++
- React, Django, Flask
- Docker, Git, AWS
- Communication, Leadership, Problem-Solving

Experience
Software Engineer, Acme Inc. | New York, NY | Jan 2020 - Present
- Developed and maintained web applications.

Junior Software Engineer, Example Corp | San Francisco, CA | Jul 2018 - Dec 2019
- Assisted in the development of mobile applications.

Education
Bachelor of Science in Computer Science, University of Example | Sep 2015 - May 2019
"""
        self.parser = ResumeParser(self.resume_text)

    def test_extract_skills(self):
        skills = self.parser.extract_skills()
        self.assertIn("Python", skills["technical"])
        self.assertIn("Java", skills["technical"])
        self.assertIn("C++", skills["technical"])
        self.assertIn("React", skills["frameworks"])
        self.assertIn("Django", skills["frameworks"])
        self.assertIn("Flask", skills["frameworks"])
        self.assertIn("Docker", skills["tools"])
        self.assertIn("Git", skills["tools"])
        self.assertIn("AWS", skills["tools"]) # Corrected assertion to expect uppercase
        self.assertIn("Communication", skills["soft"])
        self.assertIn("Leadership", skills["soft"])
        self.assertIn("Problem-Solving", skills["soft"])
        self.assertNotIn("JavaScript", skills["technical"]) # Ensure old skills are not present if text changed
        self.assertNotIn("React", skills["technical"]) # Ensure correct categorization

    def test_extract_summary(self):
        summary = self.parser.extract_summary()
        self.assertEqual(summary, "A highly motivated software engineer with 5 years of experience.")

    def test_extract_personal_info(self):
        personal_info = self.parser.extract_personal_info()
        self.assertEqual(personal_info["full_name"], "John Doe")
        self.assertEqual(personal_info["email"], "john.doe@example.com")
        self.assertEqual(personal_info["phone"], "123-456-7890")
        self.assertEqual(personal_info["location"], "New York, NY")
        self.assertEqual(personal_info["linkedin"], "linkedin.com/in/johndoe")
        self.assertEqual(personal_info["github"], "github.com/johndoe")

    def test_calculate_total_experience(self):
        parsed_data = self.parser.parse()
        total_experience = parsed_data["total_experience_years"]
        self.assertGreater(total_experience, 7.5, "Total experience should be greater than 7.5 years")
        self.assertLess(total_experience, 7.65, "Total experience should be less than 7.65 years")

if __name__ == '__main__':
    unittest.main()
