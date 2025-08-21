# Book Library Management API

This is a backend API to manage a digital book library.

## How to run

1. Install requirements.
2. Configure PostgreSQL in `db.py`.
3. Run with: uvicorn main:app --reload

## API Endpoints

- POST /books/ to add books
- GET /books/ to list books with filters
- GET /books/{id} to get book details
- PATCH /books/{id} to update book info
- DELETE /books/{id} to delete books
