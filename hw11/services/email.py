from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from hw11.services.auth import auth_service
from hw11.conf.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    Send an email for email verification.

    Args:
        email (EmailStr): Email address of the recipient.
        username (str): Username of the recipient.
        host (str): Base URL of the application.

    Raises:
        ConnectionErrors: If there is an error in establishing a connection for sending the email.
    """
    try:
        # Generate email verification token
        token_verification = auth_service.create_email_token({"sub": email})
        
        # Create message schema
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username,
                           "token": token_verification},
            subtype=MessageType.html
        )

        # Initialize FastMail instance
        fm = FastMail(conf)
        
        # Send email
        await fm.send_message(message, template_name="email_template.html")
    
    except ConnectionErrors as err:
        print(err)
