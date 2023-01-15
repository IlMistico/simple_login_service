from typing import Dict

from src.models.users import User

users_db: Dict[str, User] = {}


def insert(user: User) -> User | None:
    """
    Inserts a user in the database.
    Does not check if the user already exists.
    Return: the user if correctly created, else None

    """
    users_db[user.email] = user
    return users_db.get(user.email)


def find(email: str) -> User | None:
    """
    Finds a user by email
    Return: the user if found, else None
    """
    return users_db.get(email)


def update(email: str, update_map: Dict[str, str]) -> User | None:
    if user_db := users_db.get(email):
        user_dict = user_db.dict()
        for key, updated_value in update_map.items():
            if key in User.__fields__:
                user_dict[key] = updated_value
        updated_user = User(**user_dict)
        users_db[email] = updated_user
        return updated_user
    else:
        return None
