from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from hw11.database.models import Contact, User
from hw11.schemas import ContactModel
from datetime import date, timedelta


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieve contacts belonging to a specific user.

    Args:
    skip (int): Number of records to skip.
    limit (int): Maximum number of records to retrieve.
    user (User): User whose contacts are to be retrieved.
    db (Session): Database session.

    Returns:
    List[Contact]: List of contacts belonging to the user.
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(db: Session, user: User, first_name: str = None, last_name: str = None, email: str = None) -> Contact:
    """
    Retrieve a specific contact belonging to a user based on given criteria.

    Args:
    db (Session): Database session.
    user (User): User whose contact is to be retrieved.
    first_name (str, optional): First name of the contact. Defaults to None.
    last_name (str, optional): Last name of the contact. Defaults to None.
    email (str, optional): Email address of the contact. Defaults to None.

    Returns:
    Contact: The contact matching the specified criteria.
    """
    query = db.query(Contact)
    if first_name:
        query = query.filter(and_(Contact.first_name.ilike(
            f"%{first_name}%"), Contact.user_id == user.id))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Create a new contact for a user.

    Args:
    body (ContactModel): Contact details.
    user (User): User for whom the contact is to be created.
    db (Session): Database session.

    Returns:
    Contact: The newly created contact.
    """
    contact = Contact(first_name=body.first_name, last_name=body.last_name,
                      email=body.email, phone=body.phone, birthday=body.birthday, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    """
    Update an existing contact belonging to a user.

    Args:
    contact_id (int): ID of the contact to be updated.
    body (ContactModel): Contact details for update.
    user (User): User to whom the contact belongs.
    db (Session): Database session.

    Returns:
    Contact | None: The updated contact if found, otherwise None.
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Remove a contact belonging to a user.

    Args:
    contact_id (int): ID of the contact to be removed.
    user (User): User to whom the contact belongs.
    db (Session): Database session.

    Returns:
    Contact | None: The removed contact if found, otherwise None.
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def upcoming_birthdays(user: User, db: Session) -> List[Contact]:
    """
    Retrieve contacts of a user whose birthdays are within the next 7 days.

    Args:
    user (User): User whose contacts' upcoming birthdays are to be retrieved.
    db (Session): Database session.

    Returns:
    List[Contact]: List of contacts with upcoming birthdays.
    """
    today = date.today()
    end_date = today + timedelta(days=7)

    return db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            Contact.birthday >= today,
            Contact.birthday <= end_date
        )
    ).all()
