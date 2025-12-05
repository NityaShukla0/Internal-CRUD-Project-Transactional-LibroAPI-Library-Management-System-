from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


# ===========================
# BOOK
# ===========================

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publication_year: int


class BookCreate(BookBase):
    total_copies: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    total_copies: Optional[int] = None


class Book(BookBase):
    id: int
    total_copies: int
    available_copies: int

    model_config = ConfigDict(from_attributes=True)


# ===========================
# USER
# ===========================

class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ===========================
# LOAN
# ===========================

class BookBorrowRequest(BaseModel):
    user_id: int


class Loan(BaseModel):
    id: int
    book_id: int
    user_id: int
    status: str
    borrowed_at: datetime
    returned_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)