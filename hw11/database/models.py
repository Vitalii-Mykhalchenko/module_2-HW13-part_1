from sqlalchemy import Column, Integer, String, func, UniqueConstraint, ForeignKey, Boolean
from sqlalchemy.sql.sqltypes import Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    """
    Represents a contact in the application.

    Attributes:
    id (int): The unique identifier for the contact.
    first_name (str): The first name of the contact.
    last_name (str): The last name of the contact.
    email (str): The email address of the contact.
    phone (str): The phone number of the contact.
    birthday (datetime.date): The birthday of the contact.
    user_id (int): The ID of the user to whom the contact belongs.
    user (User): The user to whom the contact belongs.
    """
    __tablename__ = "contacts"
    __table_args__ = (
        UniqueConstraint('id', 'user_id', name='unique_tag_user'),
    )
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=False)
    birthday = Column(Date, nullable=False)
    user_id = Column('user_id', ForeignKey(
        'users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="tags")


class User(Base):
    """
    Represents a user in the application.

    Attributes:
    id (int): The unique identifier for the user.
    username (str): The username of the user.
    email (str): The email address of the user.
    password (str): The password of the user.
    created_at (datetime.datetime): The timestamp when the user was created.
    avatar (str): The avatar of the user.
    refresh_token (str): The refresh token of the user.
    confirmed (bool): Indicates if the user's account is confirmed.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
