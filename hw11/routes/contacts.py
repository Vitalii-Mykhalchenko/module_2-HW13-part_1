from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter

from sqlalchemy.orm import Session

from hw11.database.db import get_db
from hw11.schemas import ContactModel, ContactResponse
from hw11.repository import contacts as repository_contacts
from hw11.database.models import User
from hw11.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/upcoming-birthdays", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def upcoming_birthdays(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve upcoming birthdays of contacts for the current user.

    Args:
    db (Session): Database session.
    current_user (User): Current user.

    Returns:
    List[ContactResponse]: List of upcoming birthdays for contacts.
    """
    contacts = await repository_contacts.upcoming_birthdays(current_user, db)
    return contacts


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve contacts for the current user.

    Args:
    skip (int): Number of records to skip.
    limit (int): Maximum number of records to retrieve.
    db (Session): Database session.
    current_user (User): Current user.

    Returns:
    List[ContactResponse]: List of contacts.
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def find_contact(db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user), first_name: str = None, last_name: str = None, email: str = None):
    """
    Retrieve a contact by its ID for the current user.

    Args:
    db (Session): Database session.
    current_user (User): Current user.
    first_name (str, optional): First name of the contact. Defaults to None.
    last_name (str, optional): Last name of the contact. Defaults to None.
    email (str, optional): Email address of the contact. Defaults to None.

    Returns:
    ContactResponse: Contact information.
    """
    contact = await repository_contacts.get_contact(db, current_user, first_name, last_name, email)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Create a new contact for the current user.

    Args:
    body (ContactModel): Contact details.
    db (Session): Database session.
    current_user (User): Current user.

    Returns:
    ContactResponse: The newly created contact.
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Update an existing contact for the current user.

    Args:
    body (ContactModel): Contact details for update.
    contact_id (int): ID of the contact to be updated.
    db (Session): Database session.
    current_user (User): Current user.

    Returns:
    ContactResponse: The updated contact.
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
               dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Remove a contact for the current user.

    Args:
    contact_id (int): ID of the contact to be removed.
    db (Session): Database session.
    current_user (User): Current user.

    Returns:
    ContactResponse: The removed contact.
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


