from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Add the parent directory to the path to import the parser module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser.resume_parser import ResumeParser

app = FastAPI()

class ResumeRequest(BaseModel):
    resume_text: str

@app.post("/parse-resume")
async def parse_resume(request: ResumeRequest):
    parser = ResumeParser(request.resume_text)
    return parser.parse()

@app.get("/")
def read_root():
    return {"message": "Resume Parser AI API is running."}
