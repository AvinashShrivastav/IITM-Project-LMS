from flask import Flask, render_template, redirect, url_for, request, send_file, jsonify, flash
from flask import current_app as app
from .models import *
from datetime import datetime, timedelta
from io import BytesIO
from sqlalchemy.sql import func
import matplotlib.pyplot as plt
from sqlalchemy import or_

# from .models import User, Book, Section

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        this_user = User.query.filter_by(name=name).first()
        if this_user:
            if this_user.password == password:
                if this_user.role == 'librarian':
                    return redirect('/librarian')
                return redirect(f'/user/{this_user.id}')
            else:
                return render_template('user_login.html',error = 'Invalid password')
        else:
            return render_template('user_login.html',error = 'Invalid username')
    return render_template('user_login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        this_user = User.query.filter_by(name=name).first()
        if this_user:
            return render_template('user_registration.html',error = 'Username already exists')
        else:
            new_user = User(name = name, password = password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('user_registration.html')

# @app.route('/dashboard', methods=['GET', 'POST'])
# def dashboard():
#     return render_template('user_dashboard.html')

@app.route('/books<int:user_id>', methods=['GET', 'POST'])
def books(user_id):
    books = Book.query.all()
    user = User.query.get(user_id)
    return render_template('user_books.html', books = books, user = user)

@app.route('/download/<int:book_id>', methods=['GET', 'POST'])
def download(book_id):
    book = Book.query.get(book_id)
    return send_file(BytesIO(book.content), as_attachment=True, download_name=f'{book.name}.pdf')
@app.route('/viewbook/<int:book_id>', methods=['GET'])
def viewbook(book_id):
    book = Book.query.get(book_id)
    return send_file(BytesIO(book.content), mimetype='application/pdf', as_attachment=False, download_name=f'{book.name}.pdf')



@app.route('/request/<int:user_id>/<int:book_id>', methods=['GET', 'POST'])
def request_book(user_id,book_id):

    # Assuming this is inside a Flask route function
    book = Book.query.get(book_id)
    user = User.query.get(user_id)
    if not book or not user:
        return redirect('/some-error-page')

    if request.method == 'POST':
        # Check if the book is already issued and not returned
        existing_issue = BookIssue.query.filter_by(book_id=book_id, user_id=user.id).filter(BookIssue.status.in_(['issued', 'hold'])).first()
        if existing_issue:
            if existing_issue.status == 'issued':
                message = "You have already issued this book."
            elif existing_issue.status == 'hold':
                message = "You have already placed this book on hold."
            return message

        # Check if the user has already issued 5 or more books
        issued_books_count = BookIssue.query.filter_by(user_id=user_id, status='hold').count()
        if issued_books_count >= 5:
            # You can use flash to show a message to the user or handle this case as needed
            return "You cannot request more than 5 books."

        req_days = int(request.form.get('req_days'))
        issue_date = datetime.now()
        return_date = issue_date + timedelta(days=req_days)
        
        # Create a new BookIssue instance
        new_issue = BookIssue(book_id=book_id, user_id=user_id, issue_date=issue_date, return_date=return_date, status='hold')
        
        # Add the new issue to the session and commit
        db.session.add(new_issue)
        db.session.commit()
        return "Book Requested Successfully"
    return render_template('request_send.html', book = book, user = user)


@app.route('/userprofile/<int:user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    user = User.query.get(user_id)
    book_issues = BookIssue.query.filter_by(user_id=user_id).all()
    books = [Book.query.get(book_issue.book_id) for book_issue in book_issues]
    return render_template('user_dashboard.html', user = user, user_issues = book_issues)

@app.route("/cancelrequest/<int:request_id>", methods=['GET', 'POST'])
def cancel_request(request_id):
    book_issue = BookIssue.query.get(request_id)
    db.session.delete(book_issue)
    db.session.commit()
    return redirect(f'/user/{book_issue.user_id}')

@app.route('/return/<int:request_id>', methods=['GET', 'POST'])
def return_book(request_id):
    book_issue = BookIssue.query.get(request_id)
    book_issue.status = 'returned'
    book_issue.return_date = datetime.now()
    db.session.commit()
    return redirect(f'/user/{book_issue.user_id}')

@app.route('/viewbookhistory/<int:user_id>/<int:book_id>', methods=['GET', 'POST'])
def view_book_history(user_id, book_id):
    book_issues = BookIssue.query.filter_by(user_id=user_id, book_id=book_id).all()
    user = User.query.get(user_id)
    return render_template('user_book_history.html', book_issues=book_issues, user = user)

@app.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
    return "Book deleted successfully"

@app.route('/view/<int:book_id>', methods=['GET', 'POST'])
def view_book(book_id):
    # Query for the book's issue details
    book_issues = BookIssue.query.filter_by(book_id=book_id).all()

    # Pass the data to the template
    return render_template('view_book.html', book_issues=book_issues)
@app.route('/librarian', methods=['GET', 'POST'])
def librarian():
    librarian = User.query.filter_by(role='librarian').first()
    books = Book.query.all()
    sections = Section.query.all()
    return render_template('librarian_dashboard.html' , user = librarian, books = books,sections = sections)

# Function to get books by status for a user
def get_books_by_user_status(user_id, status):
    book_issues = BookIssue.query.filter_by(user_id=user_id, status=status).all()
    books = [Book.query.get(book_issue.book_id) for book_issue in book_issues]
    return books

@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user_login(user_id):
    issued_books = BookIssue.query.filter_by(user_id=user_id, status='issued').all()
    returned_books = BookIssue.query.filter_by(user_id=user_id, status='returned').all()
    hold_books = BookIssue.query.filter_by(user_id=user_id, status='hold').all()
    user = User.query.get(user_id)
    return render_template('user_mybooks.html' , user = user, issued_books = issued_books, hold_books = hold_books, returned_books = returned_books)



@app.route('/admin_req/<int:user_id>', methods=['GET', 'POST'])
def admin_req(user_id):
    user = User.query.get(user_id)
    books_on_hold = BookIssue.query.filter_by(status='hold').all()
    books_issued = BookIssue.query.filter_by(status='issued').all()
    return render_template('request_admin.html', requests=books_on_hold, issued=books_issued, user = user)
from flask import abort

@app.route('/grant/<int:request_id>', methods=['GET', 'POST'])
def grant(request_id):
    book_issue = BookIssue.query.get(request_id)
    if book_issue is None:
        abort(404)  # Not found
    book_issue.status = 'issued'
    db.session.commit()
    return redirect('/admin_req')

@app.route('/reject/<int:request_id>', methods=['GET', 'POST'])
def reject(request_id):
    book_issue = BookIssue.query.get(request_id)
    if book_issue is None:
        abort(404)  # Not found
    book_issue.status = 'rejected'
    db.session.commit()
    return redirect('/admin_req')
@app.route('/submit_feedback/<int:request_id>', methods=['GET', 'POST'])
def submit_feedback(request_id):
    book_issue = BookIssue.query.get(request_id)
    if request.method == 'POST':
        feedback = request.form.get('feedback')
        book_issue.feedback = feedback
        db.session.commit()
        return "Feedback submitted successfully"
    return render_template('submit_feedback.html', request_id = request_id)

@app.route('/revoke/<int:request_id>', methods=['GET', 'POST'])
def revoke(request_id):
    book_issue = BookIssue.query.get(request_id)
    if book_issue is None:
        abort(404)  # Not found
    book_issue.status = 'revoked'
    db.session.commit()
    return redirect('/admin_req')

@app.route('/add_section', methods=['GET', 'POST'])
def add_section():
    if request.method == 'POST':
        name = request.form.get('sec_title')
        sec_date = datetime.strptime(request.form.get('sec_date'), "%Y-%m-%d").date()
        sec_desc = request.form.get('sec_desc')
        new_section = Section(name = name, description = sec_desc, date_created = sec_date)
        db.session.add(new_section)
        db.session.commit()
        return redirect('/librarian')


@app.route('/add_book/<int:section_id>', methods=['GET', 'POST'])
def add_book(section_id):
    section = Section.query.get(section_id)
    if request.method == 'POST':
        name = request.form.get('book_name')
        authors = request.form.get('book_author')
        content = request.files['book_content'].read()
        new_book = Book(name = name, content = content)
        new_book.section = section
        for author in authors.split(','):
            new_author = Author(name = author)
            new_book.authors.append(new_author)
        db.session.add(new_book)
        db.session.commit()
        return redirect('/librarian')


@app.route('/lib_book/<int:user_id>/<int:section_id>', methods=['GET', 'POST'])
def lib_book(user_id, section_id):
    books = Book.query.filter_by(section_id = section_id).all()
    section = Section.query.get(section_id)
    user = User.query.get(user_id)
    return render_template('librarian_book.html', books = books,section = section, user = user)

@app.route('/userstats', methods=['GET', 'POST'])
def user_stats():
    # Query to get section name and count of books in each section
    section_distribution = db.session.query(
        Section.name,
        func.count(Book.id).label('book_count')
    ).join(Book.section).group_by(Section.id).all()

    # Extracting the section names and book counts for the pie chart
    section_names = [result.name for result in section_distribution]
    book_counts = [result.book_count for result in section_distribution]

    # Create the pie chart
    plt.figure(figsize=(10, 7))
    plt.pie(book_counts, labels=section_names, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Books Across Sections')

    # Save the pie chart
    plt.savefig('static/images/pie.png')
    # Step 1: Query the database
    # This query joins Section, Book, and BookIssue tables to count the number of issued books per section
    issued_books_per_section = db.session.query(
        Section.name,
        func.count(BookIssue.book_id).label('issued_count')
        ).join(Section.books).join(Book.issues).filter(BookIssue.status == 'issued').group_by(Section.name).all()
    # Step 2: Prepare data for plotting
    section_names = [result.name for result in issued_books_per_section]
    issued_counts = [result.issued_count for result in issued_books_per_section]

    # Step 3: Generate the bar chart
    plt.figure(figsize=(10, 7))  # Set the figure size
    plt.bar(section_names, issued_counts, color='skyblue')  # Create a bar chart
    plt.xlabel('Section Name')  # Label for x-axis
    plt.ylabel('Number of Books Issued')  # Label for y-axis
    plt.title('Number of Books Issued from Each Section')  # Chart title
    plt.xticks(rotation=45)  # Rotate section names for better readability
    plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
    plt.savefig('static/images/bar.png')  # Display the chart

    return render_template('user_stats.html')

@app.route('/search/<int:user_id>', methods=['GET'])
def search(user_id):
    user = User.query.get(user_id)
    query = request.args.get('query', '')
    if query:
        books = Book.query.join(Book.authors).filter(
            or_(
                Book.name.ilike(f'%{query}%'),
                Author.name.ilike(f'%{query}%')
            )
        ).distinct().all()
    else:
        # Return all books if the query is blank
        books = Book.query.all()
    return render_template('user_books.html', books=books, user=user)

@app.route('/search/<int:section_id>/<int:user_id>', methods=['GET'])
def search_section(section_id, user_id):
    user = User.query.get(user_id)
    section = Section.query.get(section_id)
    query = request.args.get('query', '')
    if query:
        books = Book.query.filter_by(section_id=section_id).join(Book.authors).filter(
            or_(
                Book.name.ilike(f'%{query}%'),
                Author.name.ilike(f'%{query}%')
            )
        ).distinct().all()
    else:
        # Return all books if the query is blank
        books = Book.query.filter_by(section_id=section_id).all()
    return render_template('librarian_book.html', books=books, section=section, user=user)

@app.route('/userdashboard')
def dashboard():
    # Fetch the current user, this is typically fetched from the session
    user = User.query.filter_by(id=1).first()  # Replace with actual user session logic

    # Fetch all books
    books = Book.query.all()

    # Get the status of each book (simplified logic)
    books_with_status = []
    for book in books:
        latest_issue = BookIssue.query.filter_by(book_id=book.id).order_by(BookIssue.issue_date.desc()).first()
        status = 'available' if not latest_issue or latest_issue.status == 'returned' else latest_issue.status
        books_with_status.append({
            'id': book.id,
            'name': book.name,
            'authors': book.authors,
            'status': status
        })

    # Fetch all sections with their books
    sections = Section.query.all()
    sections_with_books = []
    for section in sections:
        section_books = Book.query.filter_by(section_id=section.id).all()
        sections_with_books.append({
            'id': section.id,
            'name': section.name,
            'books': section_books
        })

    # Fetch books issued by the current user
    issued_books = [issue.book for issue in user.book_issues if issue.status == 'issued']

    return render_template('user_dashboard.html', user=user, books=books_with_status, sections=sections_with_books, issued_books=issued_books)

# # Add the submit_feedback route
# @app.route('/submit_feedback', methods=['POST'])
# def submit_feedback():
#     # Handle feedback submission (not implemented here)
#     pass
