from sqlalchemy.orm import Session
from typing import List, Dict
from app.utils.resume_parser import ResumeParser
from app.utils.job_matcher import JobMatcher
from app.db.models.resume import Resume
from app.db.models.job import Job
from app.services.resume_service import ResumeService


class AIService:
    """Service for AI-powered features"""

    @staticmethod
    def parse_uploaded_resume(file_path: str) -> Dict:
        """Parse an uploaded resume file"""
        parser = ResumeParser()
        return parser.parse_resume_file(file_path)

    @staticmethod
    def get_job_recommendations(db: Session, seeker_id: int, limit: int = 10) -> List[Dict]:
        """Get AI-powered job recommendations for a job seeker"""
        # Get candidate's resume
        try:
            resume = ResumeService.get_resume_by_seeker(db, seeker_id)
        except:
            return []

        # Build candidate profile
        candidate_profile = {
            "skills": [rs.skill.skill_name for rs in resume.resume_skills],
            "education": [
                {"school": edu.school_name, "degree": edu.degree}
                for edu in resume.educations
            ],
            "certifications": [
                {"name": cert.cert_name, "org": cert.issuing_organization}
                for cert in resume.certifications
            ],
            "summary": resume.about_me or ""
        }

        # Get all available jobs
        jobs = db.query(Job).all()
        job_list = [
            {
                "job_id": job.job_id,
                "job_title": job.job_title,
                "description": job.description,
                "location": job.location,
                "recruiter_id": job.recruiter_id
            }
            for job in jobs
        ]

        # Find best matches
        matcher = JobMatcher()
        matches = matcher.find_best_matching_jobs(candidate_profile, job_list, limit)

        return matches

    @staticmethod
    def intelligent_job_search(db: Session, search_description: str) -> List[Dict]:
        """AI-powered job search based on natural language description"""
        # Get all jobs
        jobs = db.query(Job).all()
        job_list = [
            {
                "job_id": job.job_id,
                "job_title": job.job_title,
                "description": job.description,
                "location": job.location
            }
            for job in jobs
        ]

        # Use AI to search
        matcher = JobMatcher()
        results = matcher.search_jobs_by_description(search_description, job_list)

        return results
