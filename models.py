from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

from database import Base


# ===========================
# ENUM
# ===========================
class LoanStatus(str, Enum):
    borrowed = "borrowed"
    returned = "returned"


# ===========================
# BOOK MODEL
# ===========================
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    publication_year = Column(Integer, nullable=False)
    total_copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)

    loans = relationship("Loan", back_populates="book")


# ===========================
# USER MODEL
# ===========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    loans = relationship("Loan", back_populates="user")


# ===========================
# LOAN MODEL
# ===========================
class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(SQLAlchemyEnum(LoanStatus), nullable=False, default=LoanStatus.borrowed)
    returned = Column(Boolean, default=False)

    borrowed_at = Column(DateTime, default=datetime.utcnow)
    returned_at = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="loans")
    user = relationship("User", back_populates="loans")