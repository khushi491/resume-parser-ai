import re

def split_into_sections(resume_text):
    # This regex looks for common section headers followed by a newline,
    # or the start of the string. It captures the header and the content.
    # It assumes sections are separated by at least two newlines or a header.
    sections = {}
    # A list of common section headers
    section_titles = [
        "Summary", "Experience", "Education", "Skills", "Projects",
        "Certifications", "Awards", "Publications", "Interests", "Volunteer Experience"
    ]
    # Create a regex pattern to match any of the section titles
    pattern = r"^\s*(" + "|".join(section_titles) + r")\s*$"

    # Split the resume text by these section titles
    # re.split will include the delimiters (section titles) if they are captured
    # in the pattern. So we need to handle them.

    # First, normalize newlines
    resume_text = resume_text.replace('\r\n', '\n')

    # Find all section headers and their start positions
    matches = []
    for match in re.finditer(pattern, resume_text, re.MULTILINE | re.IGNORECASE):
        matches.append((match.group(1), match.start(), match.end()))

    if not matches:
        # If no explicit sections are found, treat the whole text as one section
        sections["__main__"] = resume_text.strip()
        return sections

    # Add a dummy end for the last section
    matches.append(("__END__", len(resume_text), len(resume_text)))

    for i in range(len(matches) - 1):
        title = matches[i][0].strip()
        start = matches[i][2] # Start after the title
        end = matches[i+1][1] # End before the next title

        content = resume_text[start:end].strip()
        if content:
            sections[title] = content
    
    return sections
