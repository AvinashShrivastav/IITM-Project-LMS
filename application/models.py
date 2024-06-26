from .database import db
from datetime import datetime

# Define a User model
class User(db.Model):
    # A user has an id, a name, a role, and a list of books
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default = 'user') # librarian or student
    password = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='users', lazy=True, secondary = 'book_issue') # relationship with Book

# Define a Book model
class Book(db.Model):
    # A book has an id, a name, a content, an author, a date issued, a return date, and a user id
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.LargeBinary, nullable=False)
    authors = db.relationship('Author', secondary='book_author', backref='books', lazy=True) # relationship with Author
    # A book can belong to only one section, and a section can have many books
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=True) # foreign key to Section
    # Define a relationship between Book and Section
    section = db.relationship('Section', backref='books', lazy=True)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
class BookAuthor(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), primary_key=True)


class BookIssue(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='available')  # available, issued, or hold, or returned
    feedback = db.Column(db.Text, nullable=True)  
    # Define relationships to Book and User
    book = db.relationship('Book', backref='issues', lazy=True)
    user = db.relationship('User', backref='book_issues', lazy=True)


# Define a Section model
class Section(db.Model):
    # A section has an id, a name, a date created, and a description
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.now())
    description = db.Column(db.Text, nullable=True)

