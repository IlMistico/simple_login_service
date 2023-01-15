import logging
import secrets

logger = logging.getLogger(__name__)


def generate_otp(n_bytes=3):
    return secrets.token_hex(n_bytes)


def send_otp(email, otp):
    logger.info(f"OTP sent to {email}: {otp}")
