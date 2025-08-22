from pydantic import BaseModel
from typing import Optional


class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    page_count: int
    publication_year: int
    description: str


class BookCreate(BookBase):
    cover_image: Optional[str] = None


class Book(BookBase):
    id: int
    cover_image: Optional[str] = None

    class Config:
        orm_mode = True  


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    page_count: Optional[int] = None
    publication_year: Optional[int] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None  

    class Config:
        orm_mode = True
