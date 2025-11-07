# app/services/email_service.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from sanic import Sanic

from app.utils.logger_utils import get_logger

logger = get_logger(__name__)


class EmailService:
    """
    Service to send emails via an SMTP server (configured for Gmail).
    """
    def __init__(self, app: Optional[Sanic] = None):
        self.app = app
        self.config = None
        if app:
            self.init_app(app)

    def init_app(self, app: Sanic):
        """Initializes the service with Sanic app configuration."""
        self.app = app
        self.config = app.config
        logger.info("EmailService initialized.")

    async def _send_email(self, to_email: str, subject: str, html_content: str):
        """
        Connects to the SMTP server and sends the email.
        """
        if not all([
            self.config.get("EMAIL_HOST"),
            self.config.get("EMAIL_PORT"),
            self.config.get("EMAIL_SENDER"),
            self.config.get("EMAIL_PASSWORD"),
        ]):
            logger.error("[EMAIL] Email service is not configured. Please set EMAIL_* environment variables.")
            return

        sender_email = self.config.EMAIL_SENDER
        password = self.config.EMAIL_PASSWORD

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = to_email
        message.attach(MIMEText(html_content, "html"))

        try:
            with smtplib.SMTP(self.config.EMAIL_HOST, self.config.EMAIL_PORT) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, to_email, message.as_string())
            logger.info(f"Successfully sent email to {to_email} with subject '{subject}'")
        except smtplib.SMTPAuthenticationError:
            logger.error(f"[EMAIL] Authentication failed for {sender_email}. Check EMAIL_SENDER and EMAIL_PASSWORD.")
        except Exception as e:
            logger.error(f"[EMAIL] Failed to send email to {to_email}. Error: {e}")

    async def send_otp(self, email: str, otp_code: str, action: str):
        """
        Constructs and sends an OTP email.
        """
        if action.upper() == "REGISTER":
            subject = "Welcome! Your Verification Code"
            body_html = f"""
            <html>
            <body>
                <h2>Welcome to Our Service!</h2>
                <p>Thank you for registering. Please use the following One-Time Password (OTP) to activate your account:</p>
                <p style=\"font-size: 24px; font-weight: bold; letter-spacing: 2px;\">{otp_code}</p>
                <p>This code will expire in 5 minutes.</p>
                <p>If you did not request this, please ignore this email.</p>
            </body>
            </html>
            """
        elif action.upper() == "RESET_PASSWORD":
            subject = "Your Password Reset Code"
            body_html = f"""
            <html>
            <body>
                <h2>Password Reset Request</h2>
                <p>We received a request to reset your password. Use the following One-Time Password (OTP):</p>
                <p style=\"font-size: 24px; font-weight: bold; letter-spacing: 2px;\">{otp_code}</p>
                <p>This code will expire in 5 minutes.</p>
                <p>If you did not request this, please ignore this email and your password will remain unchanged.</p>
            </body>
            </html>
            """
        else:
            logger.warning(f"Attempted to send OTP for unknown action: {action}")
            return

        await self._send_email(to_email=email, subject=subject, html_content=body_html)

email_service = EmailService()