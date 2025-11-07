# app/services/otp_service.py
import random
from datetime import timedelta

from app.databases.redis_manager import redis_manager
from app.utils.password_utils import hash_password, verify_password
from app.exceptions import Unauthorized


class OTPService:
    _KEY_PREFIX = "otp"
    _TTL = timedelta(minutes=5)  # OTPs are valid for 5 minutes

    @classmethod
    def _get_key(cls, email: str, action: str) -> str:
        """Constructs a structured key for storing the OTP in Redis."""
        return f"{cls._KEY_PREFIX}:{action.lower()}:{email.lower()}"

    @classmethod
    async def generate_and_store_otp(cls, email: str, action: str) -> str:
        """
        Generates a 6-digit OTP, hashes it, and stores the hash in Redis with a TTL.
        Returns the plain-text OTP to be sent to the user.
        """
        otp_code = str(random.randint(100000, 999999))
        hashed_otp = hash_password(otp_code)

        key = cls._get_key(email, action)
        await redis_manager.client.setex(key, cls._TTL, hashed_otp)

        return otp_code

    @classmethod
    async def verify_otp(cls, email: str, action: str, submitted_code: str) -> bool:
        """
        Verifies the submitted OTP against the stored hash in Redis.
        If verification is successful, the OTP key is deleted to prevent reuse.
        """
        key = cls._get_key(email, action)
        stored_hash = await redis_manager.client.get(key)

        if not stored_hash:
            # OTP does not exist or has expired
            return False

        if verify_password(submitted_code, stored_hash.decode()):
            # Correct OTP, delete it immediately to prevent reuse
            await redis_manager.client.delete(key)
            return True
        
        # Incorrect OTP
        return False

otp_service = OTPService()
