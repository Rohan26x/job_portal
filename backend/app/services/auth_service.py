from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from app.db.models.user import User, UserType
from app.db.models.recruiter import Recruiter
from app.db.models.job_seeker import JobSeeker
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings


class AuthService:
    """Authentication service for user registration and login"""

    @staticmethod
    def register_user(db: Session, user_data: UserCreate, profile_data: dict) -> dict:
        """Register a new user with their profile (recruiter or job seeker)"""
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create user - password stored as plain text now
        db_user = User(
            email=user_data.email,
            password_hash=user_data.password,  # Storing plain password
            user_type=user_data.user_type
        )
        db.add(db_user)
        db.flush()  # Get user_id without committing

        # Create profile based on user type
        if user_data.user_type == UserType.recruiter.value:
            recruiter = Recruiter(
                user_id=db_user.user_id,
                company_name=profile_data.get("company_name"),
                company_description=profile_data.get("company_description")
            )
            db.add(recruiter)
        else:
            job_seeker = JobSeeker(
                user_id=db_user.user_id,
                first_name=profile_data.get("first_name"),
                last_name=profile_data.get("last_name"),
                bio=profile_data.get("bio")
            )
            db.add(job_seeker)

        db.commit()
        db.refresh(db_user)

        return {
            "user_id": db_user.user_id,
            "email": db_user.email,
            "user_type": db_user.user_type
        }

    @staticmethod
    def login_user(db: Session, login_data: UserLogin) -> Token:
        """Authenticate user and return access token"""
        # Find user by email
        user = db.query(User).filter(User.email == login_data.email).first()

        print(f"Login attempt for: {login_data.email}")
        print(f"User found: {user is not None}")

        if not user:
            print("User not found in database")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        print(f"Stored password: {user.password_hash}")
        print(f"Provided password: {login_data.password}")
        print(f"Passwords match: {user.password_hash == login_data.password}")

        # Verify password (plain text comparison now)
        if user.password_hash != login_data.password:
            print("Password verification failed")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token with user_id as integer
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {
            "sub": user.user_id,  # Make sure this is an integer
            "user_type": user.user_type
        }
        print(f"Creating token with data: {token_data}")

        access_token = create_access_token(
            data=token_data,
            expires_delta=access_token_expires
        )

        print("Login successful!")
        print(f"Token created: {access_token[:50]}...")
        return Token(access_token=access_token, token_type="bearer")
