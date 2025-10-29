from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from app.db.models.resume import Resume
from app.db.models.education import Education
from app.db.models.certification import Certification
from app.db.models.skill import Skill
from app.db.models.resume_skill import ResumeSkill
from app.schemas.resume import ResumeCreate, ResumeUpdate


class ResumeService:
    """Service for resume operations"""

    @staticmethod
    def create_resume(db: Session, resume_data: ResumeCreate, seeker_id: int) -> Resume:
        """Create a new resume"""
        # Create resume
        db_resume = Resume(
            seeker_id=seeker_id,
            about_me=resume_data.about_me
        )
        db.add(db_resume)
        db.flush()

        # Add educations
        if resume_data.educations:
            for edu in resume_data.educations:
                db_education = Education(
                    resume_id=db_resume.resume_id,
                    school_name=edu.school_name,
                    degree=edu.degree
                )
                db.add(db_education)

        # Add certifications
        if resume_data.certifications:
            for cert in resume_data.certifications:
                db_cert = Certification(
                    resume_id=db_resume.resume_id,
                    cert_name=cert.cert_name,
                    issuing_organization=cert.issuing_organization
                )
                db.add(db_cert)

        # Add skills
        if resume_data.skills:
            for skill_id in resume_data.skills:
                db_resume_skill = ResumeSkill(
                    resume_id=db_resume.resume_id,
                    skill_id=skill_id
                )
                db.add(db_resume_skill)

        db.commit()
        db.refresh(db_resume)
        return db_resume

    @staticmethod
    def get_resume_by_id(db: Session, resume_id: int) -> Resume:
        """Get resume by ID"""
        resume = db.query(Resume).filter(Resume.resume_id == resume_id).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        return resume

    @staticmethod
    def get_resume_by_seeker(db: Session, seeker_id: int) -> Resume:
        """Get resume by job seeker ID"""
        resume = db.query(Resume).filter(Resume.seeker_id == seeker_id).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found for this user"
            )
        return resume

    @staticmethod
    def update_resume(db: Session, resume_id: int, update_data: ResumeUpdate) -> Resume:
        """Update resume"""
        resume = ResumeService.get_resume_by_id(db, resume_id)

        if update_data.about_me is not None:
            resume.about_me = update_data.about_me

        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def delete_resume(db: Session, resume_id: int) -> bool:
        """Delete resume"""
        resume = ResumeService.get_resume_by_id(db, resume_id)
        db.delete(resume)
        db.commit()
        return True

    @staticmethod
    def get_or_create_skill(db: Session, skill_name: str, skill_type: str = None) -> Skill:
        """Get existing skill or create new one"""
        skill = db.query(Skill).filter(Skill.skill_name == skill_name).first()
        if not skill:
            skill = Skill(skill_name=skill_name, skill_type=skill_type)
            db.add(skill)
            db.commit()
            db.refresh(skill)
        return skill
