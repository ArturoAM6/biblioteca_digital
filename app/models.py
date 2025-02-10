from flask_login import UserMixin
from app import db
from datetime import date
from sqlalchemy import Enum
from enum import Enum as PyEnum

class User(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    books = db.relationship('Loan', backref='user', lazy='select')

    def __repr__(self):
        return f'<User {self.name}>'

class GenreEnum(PyEnum):
    FICTION = 'Fiction'
    NON_FICTION = 'Non-Fiction'
    MYSTERY = 'Mystery'
    FANTASY = 'Fantasy'
    SCIENCE_FICTION = 'Science Fiction'
    BIOGRAPHY = 'Biography'
    HISTORY = 'History'
    SELF_HELP = 'Self-Help'
    POETRY = 'Poetry'
    ROMANCE = 'Romance'
    OTHER = 'Other'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    genre = db.Column(Enum(GenreEnum, native_enum=False), default=GenreEnum.OTHER, nullable=False)
    synopsis = db.Column(db.String(300), nullable=True)
    release_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean, default=True)
    times_loaned = db.Column(db.Integer, nullable=False)
    loans = db.relationship('Loan', backref='book', lazy='select')

    def __repr__(self):
        return f'<Book {self.title}>'
    
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_date = db.Column(db.Date, nullable=False, default=date.today)
    devolution_date = db.Column(db.Date, nullable=False)
    returned = db.Column(db.Boolean, default=False)
    fine = db.Column(db.Float, default=0.0)
    fine_paid = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    def __repr__(self):
        return f'<Loan {self.id} - {self.book.title} to {self.user.name}>'