import mysql.connector
from datetime import date, timedelta

print("""WELCOME TO THE LIBRARY MANAGEMENT SYSTEM INTEGRATED with MySQL
DEVELOPED BY: ANURAG SINGH
^_^""")

"""
To use the program type your host, user, password, database in the given fields below for database connection.
Also make sure to create an empty database in MySQL of the name you edit below.
"""

# Database connection
conn = mysql.connector.connect(
    host='localhost',   # Host computer
    user='root',     # MySQL username
    password='12345',  # MySQL password
    database='lms2026'  # Database name
)

cursor = conn.cursor()

# Database initialization
def initialize_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                      BookID INT AUTO_INCREMENT PRIMARY KEY,
                      Title VARCHAR(255) NOT NULL,
                      Author VARCHAR(255) NOT NULL,
                      Year INT NOT NULL,
                      ISBN VARCHAR(13) UNIQUE NOT NULL,
                      Copies INT NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Issuers (
                      IssuerID INT AUTO_INCREMENT PRIMARY KEY,
                      FullName VARCHAR(255) NOT NULL,
                      Phone_no VARCHAR(10) UNIQUE NOT NULL,
                      Address VARCHAR(60))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS IssuedBooks (
                      IssueID INT AUTO_INCREMENT PRIMARY KEY,
                      BookID INT,
                      IssuerID INT,
                      IssueDate DATE,
                      ReturnDate DATE,
                      IsReturned VARCHAR(3) DEFAULT 'NO',
                      FOREIGN KEY (BookID) REFERENCES Books (BookID),
                      FOREIGN KEY (IssuerID) REFERENCES Issuers (IssuerID))''')
    
    conn.commit()

# Function to add a new book
def add_book(title, author, year, isbn, copies):
    try:
        cursor.execute('''INSERT INTO Books (Title, Author, Year, ISBN, Copies)
                          VALUES (%s, %s, %s, %s, %s)''', (title, author, year, isbn, copies))
        conn.commit()
        print("Book added successfully!")
    except mysql.connector.IntegrityError:
        print("Error: Book with the same ISBN already exists.")

# Function to display all books
def display_books():
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    
    if not books:
        print("No books found.")
        return
    
    print("BookID | Title | Author | Year | ISBN | Copies")
    print("-" * 50)
    for book in books:
        print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {book[5]}")

# Function to update a book's details
def update_book(book_id, title=None, author=None, year=None, isbn=None, copies=None):
    cursor.execute("SELECT * FROM Books WHERE BookID = %s", (book_id,)) #%s is a placeholder used for parameterized queries in Python. This helps prevent SQL injection by separating the SQL logic from the data.
    book = cursor.fetchone()
    
    if not book:
        print("Book not found.")
        return
    
    title = title if title else book[1] #if title is given then new title will be used else previous book[1] title is used 
    author = author if author else book[2]
    year = year if year else book[3]
    isbn = isbn if isbn else book[4]
    copies = copies if copies else book[5]
    
    cursor.execute('''UPDATE Books 
                      SET Title = %s, Author = %s, Year = %s, ISBN = %s, Copies = %s
                      WHERE BookID = %s''', (title, author, year, isbn, copies, book_id))
    conn.commit()
    print("Book updated successfully!")

# Function to delete a book
def delete_book(book_id):
    # Check if any books have been issued and not returned
    cursor.execute('''SELECT COUNT(*) FROM IssuedBooks WHERE BookID = %s AND IsReturned = 'NO' ''', (book_id,))
    issued_books = cursor.fetchone()
    
    if issued_books[0] > 0:
        print("Error: Book has been issued and is not returned. It cannot be deleted.")
        return

    try:
        cursor.execute("DELETE FROM Books WHERE BookID = %s", (book_id,))
        conn.commit()
        print("Book deleted successfully.")
    except mysql.connector.errors.IntegrityError:
        print("Error: Could not delete the book.")

# Function to register a new issuer
def register_issuer(fullname, phone_no, address):
    try:
        cursor.execute('''INSERT INTO Issuers (FullName, Phone_no, Address)
                          VALUES (%s, %s, %s)''', (fullname, phone_no, address))
        conn.commit()
        print("Issuer registered successfully!")
        cursor.execute('''SELECT IssuerID, Fullname, Address FROM Issuers
            WHERE Phone_no =%s''', (phone_no,))
        issuerdetails = cursor.fetchone()

        print("IssuerID | Full Name | Address")
        print(issuerdetails[0] , "|" , issuerdetails[1] , "|" ,  issuerdetails[2])
        print("Kindly Note your Issuer ID to return book.")


    except mysql.connector.IntegrityError:
        print("Error: Issuer with the phone_no already exists.")

# Function to issue a book
def issue_book(book_id, issuer_id):
    cursor.execute("SELECT Copies FROM Books WHERE BookID = %s", (book_id,))
    book = cursor.fetchone()
    
    if not book or book[0] <= 0:
        print("Book not available or out of stock.")
        return
    
    cursor.execute('''UPDATE Books SET Copies = Copies - 1 WHERE BookID = %s''', (book_id,))
    
    # Add book issue details and initialize IsReturned as 'NO'
    issue_date = date.today()
    cursor.execute('''INSERT INTO IssuedBooks (BookID, IssuerID, IssueDate, ReturnDate, IsReturned) 
                      VALUES (%s, %s, %s, NULL, 'NO')''', (book_id, issuer_id, issue_date))
    
    conn.commit()
    print("Book issued successfully!")
    print(f"Note: The issued book should be returned by {date.today() + timedelta(days=7)} or a fine of Rs.10/day will be charged.")

# Function to return a book
def return_book(issue_id):
    cursor.execute("SELECT ReturnDate FROM IssuedBooks WHERE IssueID = %s", (issue_id,))
    return_check = cursor.fetchone()

    if return_check[0] is not None:
        print("Book already returned.")
        return

    cursor.execute("SELECT BookID FROM IssuedBooks WHERE IssueID = %s", (issue_id,))
    issue = cursor.fetchone()

    if not issue:
        print("Invalid issue ID.")
        return
    
    return_date = date.today()
    cursor.execute('''UPDATE Books SET Copies = Copies + 1 WHERE BookID = %s''', (issue[0],))
    cursor.execute('''UPDATE IssuedBooks SET ReturnDate = %s, IsReturned = 'YES' WHERE IssueID = %s''', 
                   (return_date.strftime("%Y-%m-%d"), issue_id))

    conn.commit()
    print("Book returned successfully!")

# Function to view issued books
def view_issued_books():
    cursor.execute('''SELECT IssuedBooks.IssueID, Books.Title, Books.ISBN, Issuers.IssuerID, Issuers.FullName, IssuedBooks.IssueDate, IssuedBooks.ReturnDate, IssuedBooks.IsReturned
                      FROM IssuedBooks
                      JOIN Books ON IssuedBooks.BookID = Books.BookID
                      JOIN Issuers ON IssuedBooks.IssuerID = Issuers.IssuerID''')
    
    issued_books = cursor.fetchall()
    
    if not issued_books:
        print("No books have been issued.")
        return
    
    print("IssueID | Book Title | Book ISBN no. | IssuerID | Full Name | IssueDate | ReturnDate | IsReturned")
    print("-" * 80)
    for issue in issued_books:
        print(f"{issue[0]} | {issue[1]} | {issue[2]} | {issue[3]} | {issue[4]} | {issue[5]} | {issue[6]} | {issue[7]}")
        
def view_issuers_record():
        print("Record of those who issued books.\n")
        print("IssuerID | Fullname | Phone_no | IssueDate | ReturnDate")

        cursor.execute("SELECT issuers.IssuerID, issuers.FullName, issuers.Phone_no, issuedbooks.IssueDate, issuedbooks.ReturnDate FROM issuedbooks, issuers")
        issuers_list = cursor.fetchall()

        for names in issuers_list:
            for heads in names:
                print(heads, end = '  ')
            print()

def view_registered_issuers():
        print("IssuerID | Fullname | Phone_no | Address")

        cursor.execute("""SELECT IssuerID, Fullname, Phone_no, Address FROM issuers""")

        issued_books_list = cursor.fetchall()
        for record in issued_books_list:
            print(f"{record[0]} | {record[1]} | {record[2]} | {record[3]}")


# Main menu
def main_menu():
    while True:
        print("\n=== Library Management System ===")
        print("1. Add a new book")
        print("2. Display all books")
        print("3. Update book details")
        print("4. Delete a book")
        print("5. Register a new Issuer")
        print("6. Issue a book")
        print("7. Return a book")
        print("8. View issued books")
        print("9. View Registered Issuers")
        print("10. Exit")
        
        choice = input("Enter your choice: ")
        print()
        if choice == '1':
            title = input("Book title: ")
            author = input("Author name: ")
            year = int(input("Year of publication: "))
            isbn = input("ISBN no.: ")
            copies = int(input("Number of copies: "))
            add_book(title, author, year, isbn, copies)
            
        elif choice == '2':
            display_books()

        elif choice == '3':
            book_id = int(input("Enter book ID to update: "))
            title = input("New title (leave blank to keep current): ")
            author = input("New author (leave blank to keep current): ")
            year = input("New year (leave blank to keep current): ")
            if year:
                try:
                    year = int(year)
                except ValueError:
                    print("Invalid input for year!")
                    return

            isbn = input("Enter new ISBN (leave blank to keep current): ")
            copies = input("Enter new number of copies (leave blank to keep current): ")
            update_book(book_id, title or None, author or None, int(year) if year else None, isbn or None, int(copies) if copies else None)

        elif choice == '4':
            book_id = int(input("Enter book ID to delete: "))
            delete_book(book_id)

        elif choice == '5':
            print("* represents Mandatory fields")
            fullname = input("*Full Name: ")
            while len(fullname) < 4:
                fullname = input("Enter Full Name: ")
            phone_no = input("*Phone_no: ")
            while len(phone_no) != 10:
                phone_no = input("Enter correct Phone_no: ")
            address = input("Address: ")

            register_issuer(fullname, phone_no, address)

        elif choice == '6':
            book_id = int(input("Book ID: "))
            issuer_id = int(input("Issuer ID: "))
            issue_book(book_id, issuer_id)

        elif choice == '7':
            issue_id = int(input("Enter issue ID to return: "))
            return_book(issue_id)

        elif choice == '8':
            view_issued_books()

        elif choice == '9':
            view_registered_issuers()

        elif choice == '10':
            print("Exiting system...")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    initialize_db()
    main_menu()
