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

Experience
Software Engineer, Acme Inc. | New York, NY | Jan 2020 - Present
- Developed and maintained web applications.

Education
Bachelor of Science in Computer Science, University of Example | Sep 2015 - May 2019
"""
        self.parser = ResumeParser(self.resume_text)

    def test_extract_personal_info(self):
        personal_info = self.parser.extract_personal_info()
        self.assertEqual(personal_info["full_name"], "John Doe")
        self.assertEqual(personal_info["email"], "john.doe@example.com")
        self.assertEqual(personal_info["phone"], "123-456-7890")
        self.assertEqual(personal_info["location"], "New York, NY")
        self.assertEqual(personal_info["linkedin"], "linkedin.com/in/johndoe")
        self.assertEqual(personal_info["github"], "github.com/johndoe")

if __name__ == '__main__':
    unittest.main()
