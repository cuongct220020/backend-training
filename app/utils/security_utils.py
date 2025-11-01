# app/utils/security_utils.py
from datetime import datetime, timedelta, UTC
import uuid

import bcrypt
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError

from app.extensions import redis_manager
from app.hooks import exceptions


# -------------------- PASSWORD UTILS -------------------- #

def hash_password(plain: str) -> str:
    """Hashes a plain text password using bcrypt."""
    hashed = bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    """Verifies a plain text password against a hashed version."""
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))


# -------------------- JWT UTILS -------------------- #

def generate_jwt(
        *, # Use keyword-only arguments for clarity
        subject: str | int,
        jwt_secret: str,
        jwt_algorithm: str,
        expires_delta: timedelta,
        extra_data: dict | None = None
    ) -> str:
    """Generates a new JWT access token with a unique ID (jti)."""
    now = datetime.now(UTC)
    expire = now + expires_delta

    payload = {
        "sub": str(subject),
        "exp": expire,
        "iat": now,
        "jti": str(uuid.uuid4()),  # JWT ID - Unique identifier for this token
    }
    if extra_data:
        payload.update(extra_data)

    token = encode(payload, jwt_secret, algorithm=jwt_algorithm)
    return token


async def verify_jwt(
        *,
        token: str,
        jwt_secret: str,
        jwt_algorithm: str
    ) -> dict:
    """
    Verifies a JWT, checks it against the deny-list, and returns its payload.]
    """

    try:
        payload = decode(token, jwt_secret, algorithms=[jwt_algorithm])
        # Deny-list check
        jti = payload.get("jti")

        if not jti:
            raise exceptions.Unauthorized("Token is missing required 'jti' claim.")

        is_denied = await redis_manager.client.get(f"deny_list:jti:{jti}")


        if is_denied:
            raise exceptions.Unauthorized("Token has been revoked")

        return payload

    except ExpiredSignatureError:
        raise exceptions.Unauthorized("Token has expired")

    except InvalidTokenError:
        raise exceptions.Unauthorized("Invalid token")
