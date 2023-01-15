from pydantic import BaseModel


class User(BaseModel):
    """
    email: str
    password: str
    name: str = None
    age: int = None
    two_fa_enabled: bool = False
    otp: str = ""
    """

    email: str
    password: str
    name: str = None
    age: int = None
    two_fa_enabled: bool = False
    otp: str = ""
