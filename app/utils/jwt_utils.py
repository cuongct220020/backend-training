from datetime import datetime, timedelta, UTC
import uuid
import jwt

from app.databases.redis_manager import redis_manager
from app.exceptions import Unauthorized
from config import Config


class JWTHandler:
    """
    Utility class for creating, verifying, and revoking JWT tokens.
    Supports both Access and Refresh tokens with separate expirations.
    """

    def __init__(
        self,
        secret: str,
        algorithm: str = "HS256",
        access_exp_minutes: int = 30,
        refresh_exp_days: int = 7,
    ):
        self.secret = secret
        self.algorithm = algorithm
        self.access_exp_minutes = access_exp_minutes
        self.refresh_exp_days = refresh_exp_days

    # TOKEN CREATION
    def create_tokens(self, user_id: int) -> tuple[str, str, str, int]:
        """
        Create a pair of JWT tokens (access & refresh).
        Returns:
            (access_token, refresh_token, jti, expires_in_minutes)
        """
        jti = str(uuid.uuid4())
        now = datetime.now(UTC)

        access_exp = timedelta(minutes=self.access_exp_minutes)
        refresh_exp = timedelta(days=self.refresh_exp_days)

        access_payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + access_exp,
            "jti": jti,
            "type": "access",
        }

        refresh_payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + refresh_exp,
            "jti": str(uuid.uuid4()),
            "type": "refresh",
        }

        access_token = jwt.encode(access_payload, self.secret, algorithm=self.algorithm)
        refresh_token = jwt.encode(refresh_payload, self.secret, algorithm=self.algorithm)
        expires_in_minutes = int(access_exp.total_seconds() // 60)

        return access_token, refresh_token, jti, expires_in_minutes

    # TOKEN VERIFICATION
    async def verify(self, token: str, token_type: str = "access") -> dict:
        """
        Decode and validate a JWT token using instance configuration.
        It also verifies the token type ('access' or 'refresh').
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])

            # --- Security Enhancement: Verify token type ---
            if payload.get("type") != token_type:
                raise Unauthorized(f"Invalid token type. Expected '{token_type}'.")

            jti = payload.get("jti")
            if not jti:
                raise Unauthorized("Token missing 'jti' claim")

            # Check if the token has been revoked
            is_denied = await redis_manager.client.get(f"deny_list:jti:{jti}")
            if is_denied:
                raise Unauthorized("Token has been revoked")

            return payload

        except jwt.ExpiredSignatureError:
            raise Unauthorized("Token has expired")
        except jwt.InvalidTokenError:
            raise Unauthorized("Invalid token")

    # TOKEN REVOCATION
    async def revoke(self, jti: str, exp: datetime) -> None:
        """Adds a token's JTI to the deny-list until it naturally expires."""
        if not jti or not exp:
            return

        ttl = int((exp - datetime.now(UTC)).total_seconds())
        if ttl > 0:
            key = f"deny_list:jti:{jti}"
            await redis_manager.client.setex(key, ttl, "revoked")


# Create a single, configured instance for the entire application
# This assumes the required JWT settings are present in the Config class.
jwt_handler = JWTHandler(
    secret=Config.JWT_SECRET,
    algorithm=Config.JWT_ALGORITHM,
    access_exp_minutes=getattr(Config, 'JWT_ACCESS_TOKEN_EXPIRES_MINUTES', 30),
    refresh_exp_days=getattr(Config, 'JWT_REFRESH_TOKEN_EXPIRES_DAYS', 7)
)

