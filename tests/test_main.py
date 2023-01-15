from http import HTTPStatus
from pathlib import Path
import sys, logging
from fastapi.testclient import TestClient

ROOT = Path(__file__).parent.parent.resolve()
if not str(ROOT) in sys.path:
    sys.path.insert(0, str(ROOT))

from src.main import app
from src.models.users import User

client = TestClient(app)

mock_user_standard = User(
    **{
        "email": "test_standard@example.com",
        "password": "testpassword",
        "name": "Test",
        "age": 30,
        "two_fa_enabled": False,
    }
)


mock_user_2fa = User(
    **{
        "email": "test_2fa@example.com",
        "password": "testpassword",
        "name": "Test",
        "age": 30,
        "two_fa_enabled": True,
        "otp": "87rf54",
    }
)


def test_register_standard(mocker):
    mocker.patch("src.data.users.insert", return_value=mock_user_standard)

    response = client.post(
        "/register",
        json=mock_user_standard.dict(),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User created"}


def test_login_standard(mocker):
    mocker.patch("src.data.users.find", return_value=mock_user_standard)
    response = client.post(
        "/login/standard",
        json={
            "email": mock_user_standard.email,
            "password": mock_user_standard.password,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Logged in"}


def test_register_2fa(mocker):
    mocker.patch("src.data.users.insert", return_value=mock_user_2fa)
    mocker.patch("secrets.token_hex", return_value=mock_user_2fa.otp)

    response = client.post(
        "/register",
        json=mock_user_2fa.dict(),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User created"}


def test_login_2fa(mocker):
    mocker.patch("src.data.users.find", return_value=mock_user_2fa)
    response = client.post(
        "/login/standard",
        json={"email": mock_user_2fa.email, "password": mock_user_2fa.password},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "OTP required"}


def test_incorrect_otp(mocker):
    mocker.patch("src.data.users.find", return_value=mock_user_2fa)
    response = client.post(
        "/login/2fa",
        json={
            "email": mock_user_2fa.email,
            "password": mock_user_2fa.password,
            "otp": "incorrect_otp",
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect OTP"}


def test_correct_otp(mocker):
    mocker.patch("src.data.users.find", return_value=mock_user_2fa)
    response = client.post(
        "/login/2fa",
        json={
            "email": mock_user_2fa.email,
            "password": mock_user_2fa.password,
            "otp": mock_user_2fa.otp,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Logged in"}
