from sqlalchemy.orm import Session
from typing import List, Optional
from models import Book
from schemas import BookCreate, BookUpdate

def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 10) -> List[Book]:
    return db.query(Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()

def delete_book(db: Session, book_id: int) -> Optional[Book]:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return None
    db.delete(book)
    db.commit()
    return book

def search_books(db: Session, query: str, skip: int = 0, limit: int = 10) -> List[Book]:
    q = f"%{query.lower()}%"
    return db.query(Book).filter(
        (Book.title.ilike(q)) | (Book.author.ilike(q))
    ).offset(skip).limit(limit).all()

def update_book(db: Session, book_id: int, book_update: BookUpdate) -> Optional[Book]:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return None

    update_data = book_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book
