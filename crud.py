from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

import models
import schemas


# =========================================================
# BOOK CRUD
# =========================================================

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        publication_year=book.publication_year,
        total_copies=book.total_copies,
        available_copies=book.total_copies
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session):
    return db.query(models.Book).all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    db_book = get_book(db, book_id)
    if not db_book:
        return None

    diff = book.total_copies - db_book.total_copies
    if diff > 0:
        db_book.available_copies += diff

    db_book.title = book.title
    db_book.author = book.author
    db_book.isbn = book.isbn
    db_book.publication_year = book.publication_year
    db_book.total_copies = book.total_copies

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted"}


# =========================================================
# USER CRUD
# =========================================================

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# =========================================================
# LOAN LOGIC
# =========================================================

def borrow_book(db: Session, book_id: int, user_id: int):
    book = get_book(db, book_id)
    if not book or book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book not available")

    loan = models.Loan(
        book_id=book_id,
        user_id=user_id,
        status=models.LoanStatus.borrowed,
        returned=False,
        borrowed_at=datetime.utcnow()
    )

    book.available_copies -= 1

    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def return_book(db: Session, loan_id: int):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan or loan.returned:
        raise HTTPException(status_code=400, detail="Invalid loan")

    loan.returned = True
    loan.status = models.LoanStatus.returned
    loan.returned_at = datetime.utcnow()

    book = get_book(db, loan.book_id)
    book.available_copies += 1

    db.commit()
    db.refresh(loan)

    # ✅ Add return_date attribute for compatibility with tests
    loan.return_date = loan.returned_at

    return loan