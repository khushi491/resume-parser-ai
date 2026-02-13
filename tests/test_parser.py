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
- Python
- JavaScript
- Django
- React

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
        self.assertIn("JavaScript", skills["technical"])
        self.assertIn("Django", skills["technical"])
        self.assertIn("React", skills["technical"])

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
        # We need to consider the current date for "Present"
        # For a stable test, we'll calculate based on fixed dates for the past experience
        # and then add the duration from Jan 2020 to a fixed "now" date if needed.
        # However, the ExperienceCalculator already handles datetime.now() for "Present".
        # Jan 2020 - Present (let's assume current date is Feb 2026, roughly 6 years and 1 month)
        # Jul 2018 - Dec 2019 (1 year and 6 months = 1.5 years)
        # Total should be around 7.5 years, but the calculation is more precise.
        # Using a sample resume for testing total_experience_years for accuracy.

        # For the purpose of this test, let's fix "Present" to a specific date for consistent testing
        # The ExperienceCalculator uses datetime.now(), so the exact number will vary.
        # Let's verify it's a reasonable number based on the provided sample.
        # From Jan 2020 to Feb 2026 is 6 years and 1 month (approx 6.08 years)
        # From Jul 2018 to Dec 2019 is 1 year and 6 months (1.5 years)
        # Total should be ~ 7.58 years

        parsed_data = self.parser.parse()
        total_experience = parsed_data["total_experience_years"]
        # Allow for some floating point inaccuracy. Expecting around 7.58 years.
        # The exact value depends on the execution date due to 'Present'.
        # Let's assert it's within a reasonable range, e.g., > 6 and < 8
        self.assertGreater(total_experience, 7.5, "Total experience should be greater than 7.5 years")
        self.assertLess(total_experience, 7.65, "Total experience should be less than 7.65 years")

if __name__ == '__main__':
    unittest.main()
