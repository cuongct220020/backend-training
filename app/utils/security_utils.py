import os
from datetime import datetime, timedelta, UTC

import bcrypt
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError  # <-- import đúng chỗ

from app.hooks import exceptions
from main import app


# -------------------- PASSWORD UTILS -------------------- #

def hash_password(plain: str) -> str:
    """Hashes a plain text password using bcrypt."""
    hashed = bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    """Verifies a plain text password against a hashed version."""
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))


# -------------------- JWT UTILS -------------------- #

def generate_jwt(subject: str | int, extra_data: dict | None = None, expires_delta: timedelta | None = None) -> str:
    """Generates a new JWT access token with extra data in the payload."""
    now = datetime.now(UTC)
    expire = now + (expires_delta or timedelta(minutes=app.config.ACCESS_TOKEN_EXPIRE_MINUTES))

    payload = {
        "sub": str(subject),
        "exp": expire,
        "iat": now
    }
    
    if extra_data:
        payload.update(extra_data)

    token = jwt.encode(payload, app.config.JWT_SECRET, algorithm=app.config.JWT_ALGORITHM)
    return token


def verify_jwt(token: str, jwt_secret: str | None = None) -> dict:
    """
    Verifies a JWT token and returns its payload.
    Handles exceptions for expired or invalid tokens.
    """
    try:
        if jwt_secret is None:
            jwt_secret = app.config.JWT_SECRET

        # decode via jwt.decode
        payload = jwt.decode(token, jwt_secret, algorithms=[app.config.JWT_ALGORITHM])
        return payload

    except ExpiredSignatureError:
        # The token has expired
        raise exceptions.Unauthorized("Token has expired")

    except InvalidTokenError:
        # Any other JWT error (invalid signature, malformed token, etc.)
        raise exceptions.Unauthorized("Invalid token")
