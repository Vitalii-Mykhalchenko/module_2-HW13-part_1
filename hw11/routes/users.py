from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from hw11.database.db import get_db
from hw11.database.models import User
from hw11.repository import users as repository_users
from hw11.services.auth import auth_service
from hw11.conf.config import settings
from hw11.schemas import UserDb

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve the details of the current user.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        UserDb: Details of the current user.
    """
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    Update the avatar of the current user.

    Args:
        file (UploadFile): The avatar image file to upload.
        current_user (User): The current authenticated user.
        db (Session): Database session.

    Returns:
        UserDb: Updated details of the current user.
    """

    # Configuring Cloudinary
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    # Uploading the image to Cloudinary
    r = cloudinary.uploader.upload(
        file.file, public_id=f'NotesApp/{current_user.username}', overwrite=True)
    
    # Building URL for the uploaded image
    hw11_url = cloudinary.CloudinaryImage(f'NotesApp/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    
    # Updating the user's avatar URL in the database
    user = await repository_users.update_avatar(current_user.email, hw11_url, db)
    return user
