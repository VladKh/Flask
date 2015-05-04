from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(50), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User: %s email: %s>' % (self.name, self.email)


class BookNames(Base):
    __tablename__ = 'booknames'
    id = Column(Integer, primary_key=True)
    book_name = Column(String(120), unique=True)
    bookcase = relationship("Bookcase", backref="booknames")

    def __init__(self, book_name):
        self.book_name = book_name

    def __repr__(self):
        return '%s %s' % (self.id, self.book_name)


class Authors(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    author_name = Column(String(120), unique=True)
    bookcase = relationship("Bookcase", backref="authors")

    def __init__(self, author_name):
        self.author_name = author_name

    def __repr__(self):
        return '%s %s' % (self.id, self.author_name)


class Bookcase(Base):
    __tablename__ = 'bookcase'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('booknames.id'), nullable=False)
    authors_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    def __init__(self, authors_id, book_id):
        self.authors_id = authors_id
        self.book_id = book_id

    def __repr__(self):
        return '%s %s %s' % (self.id, self.book_id, self.authors_id)