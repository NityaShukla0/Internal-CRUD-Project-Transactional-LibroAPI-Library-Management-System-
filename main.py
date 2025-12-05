from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import Base, engine, get_db

# Create tables (only for dev)
Base.metadata.create_all(bind=engine)

app = FastAPI()


# ===========================
# BOOK ROUTES
# ===========================

@app.post("/books", response_model=schemas.Book, status_code=201)
def create_book_api(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.get("/books", response_model=list[schemas.Book])
def get_books_api(db: Session = Depends(get_db)):
    return crud.get_books(db)


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book_api(book_id: int, data: schemas.BookUpdate, db: Session = Depends(get_db)):
    return crud.update_book(db, book_id, data)


# ===========================
# USER ROUTES
# ===========================

@app.post("/users", response_model=schemas.User, status_code=201)
def create_user_api(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users", response_model=list[schemas.User])
def get_users_api(db: Session = Depends(get_db)):
    return crud.get_users(db)


# ===========================
# LOAN ROUTES
# ===========================

@app.post("/books/{book_id}/borrow", response_model=schemas.Loan)
def borrow_book_api(book_id: int, req: schemas.BookBorrowRequest, db: Session = Depends(get_db)):
    return crud.borrow_book(db, book_id, req.user_id)


@app.post("/loans/{loan_id}/return", response_model=schemas.Loan)
def return_book_api(loan_id: int, db: Session = Depends(get_db)):
    return crud.return_book(db, loan_id)