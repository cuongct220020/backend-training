import jwt
from datetime import datetime, timedelta, UTC
import uuid
from typing import Literal, Optional

from sanic import Sanic

from app.databases.redis_manager import redis_manager
from app.exceptions import Unauthorized


class JWTHandler:
    def __init__(self, app: Optional[Sanic] = None):
        if app:
            self.init_app(app)

    def init_app(self, app: Sanic):
        self.app = app
        self.config = app.config
        self.redis = redis_manager

    def _get_config_value(self, key: str, default=None):
        return self.config.get(key, default)

    def create_tokens(self, user_id: str, user_role: str | None = None):
        access_token_jti = str(uuid.uuid4())
        refresh_token_jti = str(uuid.uuid4())

        access_expires_delta = timedelta(minutes=self._get_config_value('JWT_ACCESS_TOKEN_EXPIRES_MINUTES', 15))
        refresh_expires_delta = timedelta(days=self._get_config_value('JWT_REFRESH_TOKEN_EXPIRES_DAYS', 30))

        issued_at_time = datetime.now(UTC)

        access_payload = {
            'token_type': 'access',
            'exp': issued_at_time + access_expires_delta,
            'iat': issued_at_time,
            'jti': access_token_jti,
            'sub': str(user_id),
            'role': user_role
        }

        refresh_payload = {
            'token_type': 'refresh',
            'exp': issued_at_time + refresh_expires_delta,
            'iat': issued_at_time,
            'jti': refresh_token_jti,
            'sub': str(user_id),
            'role': user_role
        }

        secret_key = self._get_config_value('JWT_SECRET')
        algorithm = self._get_config_value('JWT_ALGORITHM')

        access_token = jwt.encode(access_payload, secret_key, algorithm=algorithm)
        refresh_token = jwt.encode(refresh_payload, secret_key, algorithm=algorithm)

        return (
            access_token,
            refresh_token,
            access_token_jti,
            refresh_token_jti,
            access_expires_delta.total_seconds() / 60
        )

    async def verify(self, token: str, token_type: Literal['access', 'refresh'] = 'access', check_revocation: bool = True):
        secret_key = self._get_config_value('JWT_SECRET')
        algorithm = self._get_config_value('JWT_ALGORITHM')

        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Token has expired")
        except jwt.InvalidTokenError:
            raise Unauthorized("Invalid token")

        if payload.get('token_type') != token_type:
            raise Unauthorized(f"Invalid token type. Expected '{token_type}'.")

        if check_revocation:
            # 1. Check for global revocation (password change, etc.)
            user_id = payload.get('sub')
            iat = payload.get('iat')
            global_revoke_key = f"user_revoke_all_timestamp:{user_id}"
            last_global_revoke_ts = await self.redis.client.get(global_revoke_key)

            if last_global_revoke_ts and iat < int(last_global_revoke_ts):
                raise Unauthorized("Token has been revoked by a security event.")

            # 2. Check for individual token revocation (logout)
            jti = payload.get('jti')
            is_revoked = await self.redis.client.get(f"revoked_jti:{jti}")
            if is_revoked:
                raise Unauthorized("Token has been revoked.")

        return payload

    async def revoke(self, jti: str, exp: datetime):
        """Revokes a token by adding its JTI to a denylist in Redis with a TTL."""
        now = datetime.now(UTC)
        ttl = exp - now
        if ttl.total_seconds() > 0:
            await self.redis.client.setex(f"revoked_jti:{jti}", int(ttl.total_seconds()), "revoked")

jwt_handler = JWTHandler()

