from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    """
    Pydantic model representing contact data for creation.

    Attributes:
        first_name (str): First name of the contact. Max length: 50 characters.
        last_name (str): Last name of the contact. Max length: 50 characters.
        email (str): Email address of the contact. Max length: 100 characters.
        phone (str): Phone number of the contact. Max length: 100 characters.
        birthday (date): Birthday of the contact.
    """
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=100)
    phone: str = Field(max_length=100)
    birthday: date


class ContactResponse(ContactModel):
    """
    Pydantic model representing contact data for response.

    Attributes:
        id (int): Unique identifier of the contact.
    """
    id: int

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    """
    Pydantic model representing user data for creation.

    Attributes:
        username (str): Username of the user. Min length: 5, Max length: 16 characters.
        email (str): Email address of the user.
        password (str): Password of the user. Min length: 6, Max length: 10 characters.
    """
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """
    Pydantic model representing user data for database retrieval.

    Attributes:
        id (int): Unique identifier of the user.
        username (str): Username of the user.
        email (str): Email address of the user.
        created_at (datetime): Timestamp indicating when the user was created.
        avatar (str): URL of the user's avatar.
    """
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """
    Pydantic model representing user data for response.

    Attributes:
        user (UserDb): User data.
        detail (str): Detail message.
    """
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
    Pydantic model representing authentication token data.

    Attributes:
        access_token (str): Access token for authentication.
        refresh_token (str): Refresh token for token refreshing.
        token_type (str): Type of the token. Default: "bearer".
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    """
    Pydantic model representing a request for email verification.

    Attributes:
        email (EmailStr): Email address to be verified.
    """
    email: EmailStr
