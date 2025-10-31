import os
from datetime import datetime, timedelta, UTC

import bcrypt
import jwt
from main import app

# password
def hash_password(plain: str) -> str:
    """Hashes a plain text password using bcrypt."""
    hashed = bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    """Verifies a plain text password against a hashed version."""
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))


# jwt
def generate_jwt(subject: str | int,
                 jwt_secret: str,
                 expires_delta: timedelta | None = None) -> str:
    """Generates a new JWT access token."""
    now = datetime.now(UTC)
    if jwt_secret is None:
        jwt_secret = app.config.JWT_SECRET

    if expires_delta is None:
        expires_delta = now + (expires_delta or timedelta(minutes=app.config.ACCESS_TOKEN_EXPIRE_MINUTES))

    payload = {
        "sub": str(subject),
        "exp": expires_delta,
        "iat": now
    }

    token = jwt.encode(payload, jwt_secret, algorithm=app.config.JWT_ALGORITHM)
    return token

def verify_jwt(jwt_secret, token: str) -> dict:
    """Verifies a JWT token and returns its payload."""
    payload = jwt.decode(token, jwt_secret, algorithms=[app.config.JWT_ALGORITHM])
    return payload