import logging
from fastapi import APIRouter, HTTPException
import secrets
from http import HTTPStatus

from src.service.email import generate_otp, send_otp
from src.models.users import User
from src.data import users

auth_router = APIRouter()


logger = logging.getLogger(__name__)


@auth_router.post("/register")
async def register(user: User):
    f"""
    Endpoint to register new users.
    Registration will fail if user email is already present.
    """
    if users.find(user.email):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Email already registered"
        )
    if user.two_fa_enabled:
        user.otp = generate_otp(3)
        send_otp(user.email, user.otp)

    if users.insert(user):
        return {"message": "User created"}
    else:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error connecting to database",
        )


@auth_router.post("/login/standard")
async def login(user: User):
    f"""
    Login existing users without OTP.
    Login via this endpoint will fail if the user was created as a 2FA user.

    """
    user_db = users.find(user.email)
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect email or password"
        )
    elif not secrets.compare_digest(user.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect email or password"
        )
    elif user_db.two_fa_enabled:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="OTP required")
    else:
        # Handle successfull login
        return {"message": "Logged in"}


@auth_router.post("/login/2fa")
async def two_fa(user: User):
    f"""
    Endpoint for 2-factor authentication.
    """

    user_db = users.find(user.email)

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect email or password"
        )
    elif not secrets.compare_digest(user.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect email or password"
        )
    elif not secrets.compare_digest(user.otp, user_db.otp):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect OTP")
    else:
        # Handle successfull login
        return {"message": "Logged in"}
