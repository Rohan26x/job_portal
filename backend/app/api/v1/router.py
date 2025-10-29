from fastapi import APIRouter
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import users
from app.api.v1.endpoints import recruiters
from app.api.v1.endpoints import job_seekers
from app.api.v1.endpoints import jobs
from app.api.v1.endpoints import applications
from app.api.v1.endpoints import resumes
from app.api.v1.endpoints import ai

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(recruiters.router)
api_router.include_router(job_seekers.router)
api_router.include_router(jobs.router)
api_router.include_router(applications.router)
api_router.include_router(resumes.router)
api_router.include_router(ai.router)
