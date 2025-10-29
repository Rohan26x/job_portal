from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings


def verify_password(plain_password: str, stored_password: str) -> bool:
    """Verify a plain password (no encryption)"""
    return plain_password == stored_password


def get_password_hash(password: str) -> str:
    """Return password as-is (no hashing)"""
    return password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # Convert sub to string if it's an integer
    if "sub" in to_encode and isinstance(to_encode["sub"], int):
        to_encode["sub"] = str(to_encode["sub"])

    print(f"Encoding token with data: {to_encode}")
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"Decoded payload: {payload}")

        # Convert sub back to int
        if "sub" in payload:
            payload["sub"] = int(payload["sub"])

        return payload
    except JWTError as e:
        print(f"JWT decode error: {e}")
        return None
