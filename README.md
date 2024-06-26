# Library Management System

## Overview
The Library Management System is a multi-user application designed to manage the issuing and returning of e-books. It includes functionalities for both librarians and general users (students).

## Frameworks Used
- **Flask**: For application code
- **Jinja2 templates + Bootstrap**: For HTML generation and styling
- **SQLite**: For data storage
##Wireframe
![LIbrary_Management_Wireframe (1)](https://github.com/AvinashShrivastav/Library-Management-System/assets/110047194/1d15780e-b8bb-46bb-a090-6486218eff6a)

## Core Functionalities
### General User
- **Login/Register**: Users can create an account and log in.
- **View Sections/e-books**: Users can view all the existing sections and e-books.
- **Request/Return Books**: Users can request and return e-books.
  - A user can request a maximum of 5 e-books.
  - A user can access a book for a specific period of time (e.g., N hours/days/weeks).
    - For example, if N = 7 days, the user can return the book before 7 days. If they fail to do so, access to the book will be automatically revoked after 7 days.
- **Feedback**: Users can give feedback for an e-book.


### Librarian
- **Issue e-books**: Issue one or multiple e-books to a user.
- **Revoke access**: Revoke access for one or multiple e-books from a user.
- **Multi-language support**: Storage should handle multiple languages, usually UTF-8 encoding is sufficient for this.
- **Edit sections/e-books**: Edit an existing section or e-book.
  - Change content, author name, number of pages/volume, etc.
- **Remove sections/e-books**: Remove an existing section or e-book.
- **Assign books to sections**: Assign a book to a particular section.
- **Monitor e-book status**: A librarian can monitor the current status of each e-book and the user it is issued to.
- **Available e-books**: View available e-books in the library.

## Additional Features
- **Search Functionality**: Ability to search for sections and e-books based on various criteria.
- **Download e-books**: Users can download e-books as PDFs for a price.
- **APIs**: CRUD operations on e-books/sections and additional APIs for creating graphs for the librarian dashboard.
- **Validation**: Backend validation for all form inputs before storing/selecting from the database.

## Installation
1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the application using `python app.py`.

## Usage
1. Open the application in your local browser.
2. Register or log in as a user or librarian.
3. Use the dashboard to manage sections and e-books.

##Screenshots (Demo)
To be uploaded...


## License
This project is licensed under the MIT License.
