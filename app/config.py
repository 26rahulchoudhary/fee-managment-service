import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_SERVER = os.getenv("DATABASE_SERVER")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_DRIVER = os.getenv(
        "DATABASE_DRIVER",
        "ODBC Driver 18 for SQL Server",
    )

    @classmethod
    def validate(cls):
        required = {
            "DATABASE_SERVER": cls.DATABASE_SERVER,
            "DATABASE_NAME": cls.DATABASE_NAME,
            "DATABASE_USERNAME": cls.DATABASE_USERNAME,
            "DATABASE_PASSWORD": cls.DATABASE_PASSWORD,
        }

        missing = [
            key for key, value in required.items()
            if not value
        ]

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )


settings = Settings()