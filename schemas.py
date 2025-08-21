from pydantic import BaseModel
from typing import Optional

# Base properties shared for creating or updating books
class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    page_count: int
    publication_year: int
    description: str

# Used when creating a new book, optional cover image filename/path included
class BookCreate(BookBase):
    cover_image: Optional[str] = None

# Used when returning book data from the API (includes ID)
class Book(BookBase):
    id: int
    cover_image: Optional[str] = None

    class Config:
        orm_mode = True  # This tells Pydantic to read data easily from ORM objects (SQLAlchemy)

# New schema for updating existing book (all fields optional)
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    page_count: Optional[int] = None
    publication_year: Optional[int] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None  # Optional field included if you want to update image path

    class Config:
        orm_mode = True
