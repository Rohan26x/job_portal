import PyPDF2
from typing import Dict, List, Optional
from openai import OpenAI
from app.core.config import settings
import json


class ResumeParser:
    """AI-powered resume parser using OpenAI"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def parse_resume_with_ai(self, resume_text: str) -> Dict:
        """Parse resume text using OpenAI to extract structured information"""

        prompt = f"""
        You are a resume parser. Extract the following information from the resume text provided.
        Return the data in JSON format with these exact keys:
        - personal_info (dict with: first_name, last_name, email, phone)
        - skills (list of strings)
        - education (list of dicts with: school_name, degree, field_of_study)
        - certifications (list of dicts with: cert_name, issuing_organization)
        - work_experience (list of dicts with: company, position, duration, description)
        - summary (string: brief professional summary)

        Resume Text:
        {resume_text}

        Return only valid JSON, no additional text.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are a professional resume parser that extracts structured data from resumes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )

            result = response.choices[0].message.content
            # Parse JSON response
            parsed_data = json.loads(result)
            return parsed_data

        except Exception as e:
            print(f"Error parsing resume with AI: {e}")
            return {
                "personal_info": {},
                "skills": [],
                "education": [],
                "certifications": [],
                "work_experience": [],
                "summary": ""
            }

    def parse_resume_file(self, file_path: str) -> Dict:
        """Complete resume parsing pipeline"""
        # Extract text from PDF
        resume_text = self.extract_text_from_pdf(file_path)

        if not resume_text:
            return {"error": "Could not extract text from resume"}

        # Parse with AI
        parsed_data = self.parse_resume_with_ai(resume_text)
        return parsed_data
