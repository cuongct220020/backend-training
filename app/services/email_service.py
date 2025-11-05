# app/services/email_service.py
from app.utils.logger_utils import get_logger

logger = get_logger(__name__)

class EmailService:
    """
    A mock email service for sending communications.
    In a real-world application, this would integrate with a third-party
    email provider like SendGrid, AWS SES, etc.
    """

    @staticmethod
    async def send_otp(email: str, otp_code: str, action: str):
        """
        Sends an OTP code to the specified email address.

        :param email: The recipient's email address.
        :param otp_code: The One-Time Password to be sent.
        :param action: The context of the OTP (e.g., 'register', 'reset_password').
        """
        # TODO: Replace this with a real email sending implementation.
        # For development and testing purposes, we will just log the OTP.
        logger.info(f"[MOCK EMAIL] Sending OTP to {email} for action '{action}'. Code: {otp_code}")
        
        # Simulate a network call
        import asyncio
        await asyncio.sleep(0.1) 

        # In a real implementation, you would handle potential errors from the email provider here.
        # For example, if the email service is down, you might want to raise a ServiceUnavailable exception.
        
        logger.info(f"[MOCK EMAIL] Successfully sent OTP to {email}")

# A single, shared instance for the entire application
email_service = EmailService()
