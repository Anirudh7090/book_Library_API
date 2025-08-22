from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query, Form, Body, Path
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
import json

import models, schemas, crud, utils
from db import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Library Management API")


STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.middleware("http")
async def log_requests(request, call_next):
    utils.log_info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    utils.log_info(f"Completed request: {request.method} {request.url} with status {response.status_code}")
    return response


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: str = Form(...),  # Accept JSON string in form field 'book'
        cover_image: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db)
):
    
    book_data = json.loads(book)
    book_obj = schemas.BookCreate(**book_data)

    
    if cover_image:
        file_location = f"{STATIC_DIR}/{cover_image.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(cover_image.file, buffer)
        book_obj.cover_image = file_location

    created_book = crud.create_book(db, book_obj)
    utils.log_info(f"Created book '{created_book.title}' by {created_book.author}")
    return created_book


@app.get("/books/", response_model=List[schemas.Book])
def list_books(
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = Query(None, description="Search by title or author"),
        genre: Optional[str] = Query(None),
        author: Optional[str] = Query(None),
        db: Session = Depends(get_db)
):
    if search:
        return crud.search_books(db, search, skip, limit)
    
    query = db.query(models.Book)
    if genre:
        query = query.filter(models.Book.genre.ilike(f"%{genre}%"))
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    books = query.offset(skip).limit(limit).all()
    return books


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    # Delete cover image file if it exists
    if book.cover_image and os.path.isfile(book.cover_image):
        os.remove(book.cover_image)
    crud.delete_book(db, book_id)
    utils.log_info(f"Deleted book id {book_id}")
    return {"detail": "Book deleted successfully"}


@app.patch("/books/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int = Path(..., description="ID of the book to update"),
    book_update: schemas.BookUpdate = Body(...),
    db: Session = Depends(get_db)
):
    existing_book = crud.get_book(db, book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    updated_book = crud.update_book(db, book_id, book_update)
    return updated_book
