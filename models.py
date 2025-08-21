from sqlalchemy import Column, Integer, String
from db import Base  # Import the Base class from db.py

class Book(Base):
    __tablename__ = "books"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key, auto-incrementing
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    genre = Column(String, index=True, nullable=False)
    page_count = Column(Integer, nullable=False)
    publication_year = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    cover_image = Column(String, nullable=True)  # Optional: file path for cover image
