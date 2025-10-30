from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models.resume import Resume, Certification
from app.db.models.skill import Skill, ResumeSkill
from app.db.models.job_seeker import JobSeeker
from app.schemas.resume import ResumeCreate, ResumeUpdate


class ResumeService:

    @staticmethod
    def create_resume(db: Session, user_id: int, resume_data: ResumeCreate):
        """Create a new resume"""
        job_seeker = db.query(JobSeeker).filter(JobSeeker.user_id == user_id).first()
        if not job_seeker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job seeker profile not found"
            )

        existing_resume = db.query(Resume).filter(
            Resume.job_seeker_id == job_seeker.job_seeker_id
        ).first()

        if existing_resume:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resume already exists. Use update instead."
            )

        resume = Resume(
            job_seeker_id=job_seeker.job_seeker_id,
            about_me=resume_data.about_me
        )
        db.add(resume)
        db.flush()

        if resume_data.skills:
            for skill_name in resume_data.skills:
                skill = db.query(Skill).filter(Skill.skill_name == skill_name).first()
                if not skill:
                    skill = Skill(skill_name=skill_name)
                    db.add(skill)
                    db.flush()

                resume_skill = ResumeSkill(
                    resume_id=resume.resume_id,
                    skill_id=skill.skill_id
                )
                db.add(resume_skill)

        if resume_data.certifications:
            for cert_data in resume_data.certifications:
                certification = Certification(
                    resume_id=resume.resume_id,
                    cert_name=cert_data.cert_name,
                    issuing_organization=cert_data.issuing_organization
                )
                db.add(certification)

        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def update_resume(db: Session, resume_id: int, user_id: int, resume_data: ResumeUpdate):
        """Update an existing resume"""
        job_seeker = db.query(JobSeeker).filter(JobSeeker.user_id == user_id).first()
        if not job_seeker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job seeker profile not found"
            )

        resume = db.query(Resume).filter(
            Resume.resume_id == resume_id,
            Resume.job_seeker_id == job_seeker.job_seeker_id
        ).first()

        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )

        if resume_data.about_me is not None:
            resume.about_me = resume_data.about_me

        if resume_data.skills is not None:
            db.query(ResumeSkill).filter(ResumeSkill.resume_id == resume_id).delete()

            for skill_name in resume_data.skills:
                skill = db.query(Skill).filter(Skill.skill_name == skill_name).first()
                if not skill:
                    skill = Skill(skill_name=skill_name)
                    db.add(skill)
                    db.flush()

                resume_skill = ResumeSkill(
                    resume_id=resume.resume_id,
                    skill_id=skill.skill_id
                )
                db.add(resume_skill)

        if resume_data.certifications is not None:
            db.query(Certification).filter(Certification.resume_id == resume_id).delete()

            for cert_data in resume_data.certifications:
                certification = Certification(
                    resume_id=resume.resume_id,
                    cert_name=cert_data.cert_name,
                    issuing_organization=cert_data.issuing_organization
                )
                db.add(certification)

        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def get_resume_by_id(db: Session, resume_id: int):
        """Get resume by ID"""
        return db.query(Resume).filter(Resume.resume_id == resume_id).first()

    @staticmethod
    def get_resume_by_job_seeker(db: Session, user_id: int):
        """Get resume by job seeker user_id"""
        job_seeker = db.query(JobSeeker).filter(JobSeeker.user_id == user_id).first()
        if not job_seeker:
            return None

        return db.query(Resume).filter(
            Resume.job_seeker_id == job_seeker.job_seeker_id
        ).first()
