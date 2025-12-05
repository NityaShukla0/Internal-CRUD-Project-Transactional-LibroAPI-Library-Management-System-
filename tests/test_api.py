from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# =====================================================
# BOOK ROUTES
# =====================================================

@app.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(db: Session = Depends(get_db)):
    return crud.get_books(db)


@app.post("/books/{book_id}/borrow", response_model=schemas.Loan, status_code=status.HTTP_201_CREATED)
def borrow_book(book_id: int, request: schemas.BookBorrowRequest, db: Session = Depends(get_db)):
    loan = crud.borrow_book(db, book_id, request.user_id)
    if not loan:
        raise HTTPException(status_code=400, detail="Cannot borrow book")
    return loan


# =====================================================
# USER ROUTES
# =====================================================

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


# =====================================================
# LOAN ROUTES
# =====================================================

@app.post("/loans/{loan_id}/return", response_model=schemas.Loan)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    loan = crud.return_book(db, loan_id)
    if not loan:
        raise HTTPException(status_code=400, detail="Cannot return loan")
    return loan