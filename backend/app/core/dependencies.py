from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.user import User
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        if payload is None:
            print("Token decode returned None")
            raise credentials_exception

        user_id: int = payload.get("sub")
        print(f"Decoded token - user_id: {user_id}")

        if user_id is None:
            print("No user_id in token payload")
            raise credentials_exception

    except JWTError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception

    user = db.query(User).filter(User.user_id == user_id).first()
    print(f"Found user: {user is not None}")

    if user is None:
        print(f"No user found with ID: {user_id}")
        raise credentials_exception

    return user


def get_current_recruiter(current_user: User = Depends(get_current_user)) -> User:
    """Ensure current user is a recruiter"""
    if current_user.user_type != "recruiter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Recruiter access required."
        )
    return current_user


def get_current_job_seeker(current_user: User = Depends(get_current_user)) -> User:
    """Ensure current user is a job seeker"""
    if current_user.user_type != "job_seeker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Job seeker access required."
        )
    return current_user
