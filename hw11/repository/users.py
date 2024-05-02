from libgravatar import Gravatar
from sqlalchemy.orm import Session

from hw11.database.models import User
from hw11.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieve a user by their email address.

    Args:
    email (str): Email address of the user to retrieve.
    db (Session): Database session.

    Returns:
    User: The user corresponding to the provided email address.
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Create a new user.

    Args:
    body (UserModel): User details.
    db (Session): Database session.

    Returns:
    User: The newly created user.
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Update the refresh token for a user.

    Args:
    user (User): The user for whom the token is to be updated.
    token (str | None): The new refresh token or None if removing the token.
    db (Session): Database session.
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirm a user's email address.

    Args:
    email (str): Email address of the user to confirm.
    db (Session): Database session.
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Update a user's avatar URL.

    Args:
    email (str): Email address of the user whose avatar is to be updated.
    url (str): New avatar URL.
    db (Session): Database session.

    Returns:
    User: The updated user object.
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
