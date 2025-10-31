import os
from datetime import datetime, timedelta, UTC

import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()  # Load environment variables
JWT_SECRET = os.getenv('JWT_SECRET', 'dev-secret')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))


# password
def hash_password(plain: str) -> str:
    """Hashes a plain text password using bcrypt."""
    hashed = bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    """Verifies a plain text password against a hashed version."""
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))


# jwt
def generate_jwt(subject: str | int, expires_delta: timedelta | None = None) -> str:
    """Generates a new JWT access token."""
    now = datetime.now(UTC)
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    payload = {
        "sub": str(subject),
        "exp": expire,
        "iat": now
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def verify_jwt(token: str) -> dict:
    """Verifies a JWT token and returns its payload."""
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return payload