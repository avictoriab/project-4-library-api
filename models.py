from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    books = relationship("Book", back_populates="user")