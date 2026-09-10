from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


settings.validate()


connection_string = (
    f"DRIVER={{{settings.DATABASE_DRIVER}}};"
    f"SERVER={settings.DATABASE_SERVER};"
    f"DATABASE={settings.DATABASE_NAME};"
    f"UID={settings.DATABASE_USERNAME};"
    f"PWD={settings.DATABASE_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)


DATABASE_URL = (
    "mssql+pyodbc:///?odbc_connect="
    + quote_plus(connection_string)
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()