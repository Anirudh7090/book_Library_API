from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL database URL with your credentials
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Anirudh@localhost:5432/book_library_db"

# Create database engine to connect to PostgreSQL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# SessionLocal class to create DB session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models (tables) to inherit from
Base = declarative_base()
