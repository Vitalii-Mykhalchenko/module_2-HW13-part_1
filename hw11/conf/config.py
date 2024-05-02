from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Class defining the application settings.

    Attributes:
    POSTGRES_DB (str): Name of the PostgreSQL database.
    POSTGRES_USER (str): PostgreSQL database user.
    POSTGRES_PASSWORD (int): Password for accessing the PostgreSQL database.
    POSTGRES_PORT (int): Port for connecting to the PostgreSQL database.
    sqlalchemy_database_url (str): SQLAlchemy database URL.
    secret_key (str): Secret key for encrypting session data.
    algorithm (str): Algorithm for session data encryption.
    mail_username (str): Email username.
    mail_password (str): Password for accessing email.
    mail_from (str): Sender's email address.
    mail_port (int): Port for connecting to the email server.
    mail_server (str): Email server.
    redis_host (str): Redis server host.
    redis_port (int): Redis server port.
    cloudinary_name (str): Cloudinary account name.
    cloudinary_api_key (str): Cloudinary API key.
    cloudinary_api_secret (str): Cloudinary API secret key.

    """
    POSTGRES_DB : str
    POSTGRES_USER :str
    POSTGRES_PASSWORD :int
    POSTGRES_PORT : int
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str 
    redis_port: int 
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
