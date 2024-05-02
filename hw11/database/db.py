from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hw11.conf.config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    """
    Function to retrieve a database session object.

    Returns:
    session: Database session object created based on the local session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()