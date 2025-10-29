from app.db.database import Base

# Import all models here for Alembic to detect them
from app.db.models.user import User
from app.db.models.recruiter import Recruiter
from app.db.models.job_seeker import JobSeeker
from app.db.models.job import Job
from app.db.models.application import Application
from app.db.models.resume import Resume
from app.db.models.education import Education
from app.db.models.certification import Certification
from app.db.models.skill import Skill
from app.db.models.resume_skill import ResumeSkill
