import pytest
from datetime import date, timedelta

from crud import (
    create_book,
    get_book,
    update_book,
    delete_book,
    create_user,
    get_user,
    borrow_book,
    return_book
)
from schemas import BookCreate, UserCreate
from models import Loan


# ------------------------------------------------------
# BOOK CRUD TESTS
# ------------------------------------------------------

def test_create_and_get_book(db_session):
    book_data = BookCreate(
        title="Test Book",
        author="Author",
        isbn="111-222-333",
        publication_year=2020,
        total_copies=5
    )

    created_book = create_book(db_session, book_data)
    assert created_book.id is not None
    assert created_book.available_copies == 5

    fetched_book = get_book(db_session, created_book.id)
    assert fetched_book.title == "Test Book"


def test_update_book(db_session):
    book_data = BookCreate(
        title="Old Title",
        author="Author",
        isbn="123456",
        publication_year=2020,
        total_copies=3
    )
    book = create_book(db_session, book_data)

    update_data = BookCreate(
        title="New Title",
        author="Author",
        isbn="123456",
        publication_year=2020,
        total_copies=4
    )

    updated = update_book(db_session, book.id, update_data)

    assert updated.title == "New Title"
    assert updated.total_copies == 4
    assert updated.available_copies == 4   # reset rule


def test_delete_book(db_session):
    book_data = BookCreate(
        title="To Delete",
        author="A",
        isbn="999",
        publication_year=2010,
        total_copies=2
    )
    book = create_book(db_session, book_data)

    delete_book(db_session, book.id)
    assert get_book(db_session, book.id) is None


# ------------------------------------------------------
# USER CRUD TESTS
# ------------------------------------------------------

def test_create_and_get_user(db_session):
    user_data = UserCreate(
        name="John Doe",
        email="john@example.com"
    )
    user = create_user(db_session, user_data)

    assert user.id is not None

    fetched = get_user(db_session, user.id)
    assert fetched.email == "john@example.com"


# ------------------------------------------------------
# LOAN TRANSACTION TESTS
# ------------------------------------------------------

def test_borrow_book(db_session):
    """Borrow should reduce available_copies and create a loan."""
    book = create_book(db_session, BookCreate(
        title="Borrowable",
        author="X",
        isbn="444",
        publication_year=2020,
        total_copies=1
    ))

    user = create_user(db_session, UserCreate(
        name="Borrower",
        email="b@example.com"
    ))

    loan = borrow_book(db_session, book.id, user.id)

    updated_book = get_book(db_session, book.id)

    assert loan.status == "borrowed"
    assert updated_book.available_copies == 0


def test_return_book(db_session):
    """Return should increment available_copies and close the loan."""
    book = create_book(db_session, BookCreate(
        title="Returnable",
        author="X",
        isbn="555",
        publication_year=2019,
        total_copies=1
    ))

    user = create_user(db_session, UserCreate(
        name="User",
        email="u@example.com"
    ))

    # Borrow
    loan = borrow_book(db_session, book.id, user.id)

    # Return
    returned = return_book(db_session, loan.id)
    updated_book = get_book(db_session, book.id)

    assert returned.status == "returned"
    assert updated_book.available_copies == 1
    assert returned.return_date is not None