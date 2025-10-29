from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Combined schemas for registration
class RecruiterRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=3)
    user_type: str = "recruiter"
    company_name: str
    company_description: str = ""


class JobSeekerRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=3)
    user_type: str = "job_seeker"
    first_name: str
    last_name: str
    bio: str = ""


@router.post("/register/recruiter", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_recruiter(
        data: RecruiterRegister,
        db: Session = Depends(get_db)
):
    """Register a new recruiter"""
    user_data = UserCreate(
        email=data.email,
        password=data.password,
        user_type="recruiter"
    )

    profile_data = {
        "company_name": data.company_name,
        "company_description": data.company_description
    }

    return AuthService.register_user(db, user_data, profile_data)


@router.post("/register/job-seeker", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_job_seeker(
        data: JobSeekerRegister,
        db: Session = Depends(get_db)
):
    """Register a new job seeker"""
    user_data = UserCreate(
        email=data.email,
        password=data.password,
        user_type="job_seeker"
    )

    profile_data = {
        "first_name": data.first_name,
        "last_name": data.last_name,
        "bio": data.bio
    }

    return AuthService.register_user(db, user_data, profile_data)


@router.post("/login", response_model=Token)
def login(
        login_data: UserLogin,
        db: Session = Depends(get_db)
):
    """Login user and return access token"""
    return AuthService.login_user(db, login_data)


@router.post("/token", response_model=Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """OAuth2 compatible token login"""
    login_data = UserLogin(email=form_data.username, password=form_data.password)
    return AuthService.login_user(db, login_data)
