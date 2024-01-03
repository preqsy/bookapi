from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False, unique=True)
    isbn = Column(BIGINT, nullable=False, unique=True)
    page_count = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    published_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    status = Column(Boolean, nullable=False, server_default="TRUE")
    categories = Column(String, nullable=False)
    authors = Column(
        String, ForeignKey("users.username", ondelete="CASCADE"), nullable=False
    )
    is_deleted = Column(Boolean, nullable=False, server_default="FALSE")
    owner = relationship("Users")


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_deleted = Column(Boolean, nullable=False, server_default='FALSE')


class Like(Base):
    __tablename__ = "likes"

    book_isbn = Column(
        BIGINT,
        ForeignKey("books.isbn", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )


