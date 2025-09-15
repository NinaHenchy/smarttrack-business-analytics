import os
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL",
                         "mysql+pymysql://smarttrack_user:SmartTrack2024Pass!@mysql:3306/smarttrack_db?charset=utf8mb4")


def create_engine_with_retry(database_url: str, max_retries: int = 5, retry_delay: int = 5):
    """Create database engine with connection retry logic."""

    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})")

            # SQLAlchemy 2.x compatible engine creation
            engine = create_engine(
                database_url,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=False  # Set to True for SQL debugging
            )

            # Test the connection using SQLAlchemy 2.x syntax
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("✅ Database connection successful")
                return engine

        except OperationalError as e:
            logger.warning(f"Database connection failed (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("All database connection attempts failed")
                raise


# Create engine
engine = create_engine_with_retry(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use the old declarative_base for compatibility with your models
Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()