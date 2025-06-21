import json
from typing import Dict, List
from datetime import datetime, timedelta

LATE_FEE_PER_DAY = 10
BORROW_DAYS = 14

class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._is_borrowed = False

    def borrow_book(self) -> bool:
        if not self._is_borrowed:
            self._is_borrowed = True
            return True
        return False

    def return_book(self) -> bool:
        if self._is_borrowed:
            self._is_borrowed = False
            return True
        return False

    def get_status(self):
        return "Borrowed" if self._is_borrowed else "Available"

    def __str__(self) -> str:
        return (f"Title:{self._title}\n"
                f"Author:{self._author}\n"
                f"ISBN:{self._isbn}\n"
                f"Status:{self.get_status()}")

    def to_dict(self) -> dict:
        return {
            "Title": self._title,
            "Author": self._author,
            "ISBN": self._isbn,
            "Status": self.get_status()
        }

class User:
    def __init__(self, name: str, user_id: str):
        self._name = name
        self._user_id = user_id
        self._borrowed_books: Dict[str, str] = {}  # ISBN -> due_date (ISO string)

    def add_borrowed_book(self, isbn: str, due_date: datetime) -> None:
        self._borrowed_books[isbn] = due_date.strftime('%Y-%m-%d')

    def remove_borrowed_book(self, isbn: str) -> None:
        if isbn in self._borrowed_books:
            del self._borrowed_books[isbn]

    def __str__(self) -> str:
        return (f"User:{self._name}\n"
                f"User Id:{self._user_id}\n"
                f"Borrowed books:{len(self._borrowed_books)}\n")

    def to_dict(self) -> dict:
        return {
            "User": self._name,
            "User Id": self._user_id,
            "Borrowed books": self._borrowed_books
        }

    @staticmethod
    def from_dict(data: Dict):
        user = User(data["User"], data["User Id"])
        user._borrowed_books = data.get("Borrowed books", {})
        return user

class Library:
    def __init__(self, book_file: str = 'books.json', user_file: str = 'users.json'):
        self._book_file = book_file
        self._user_file = user_file
        self._users: Dict[str, User] = {}
        self._books: Dict[str, Book] = {}
        self._load_data()
        self._load_user()

    def _load_data(self) -> None:
        try:
            with open(self._book_file, 'r') as bf:
                book_data = json.load(bf)
                for book in book_data:
                    b = Book(book['Title'], book['Author'], book['ISBN'])
                    if book.get("Status") == 'Borrowed':
                        b.borrow_book()
                    self._books[book['ISBN']] = b
        except FileNotFoundError:
            print(f"{self._book_file} not found.")

    def _load_user(self) -> None:
        try:
            with open(self._user_file, 'r') as uf:
                user_data = json.load(uf)
                for user in user_data:
                    u = User.from_dict(user)
                    self._users[u._user_id] = u
        except FileNotFoundError:
            print(f"{self._user_file} not found.")

    def _save_data(self) -> None:
        try:
            with open(self._book_file, 'w') as bf:
                books_list = [book.to_dict() for book in self._books.values()]
                json.dump(books_list, bf, indent=4)
        except Exception as e:
            print(f"Error saving book data: {e}")

        try:
            with open(self._user_file, 'w') as uf:
                users_list = [user.to_dict() for user in self._users.values()]
                json.dump(users_list, uf, indent=4)
        except Exception as e:
            print(f"Error saving user data: {e}")

    def add_book(self, book: Book) -> bool:
        if book._isbn in self._books:
            print(f"Book with ISBN {book._isbn} already exists.")
            return False
        self._books[book._isbn] = book
        self._save_data()
        print(f"Book '{book._title}' added successfully.")
        return True

    def register_user(self, user: User) -> bool:
        if user._user_id in self._users:
            print(f"User ID {user._user_id} already registered")
            return False
        self._users[user._user_id] = user
        self._save_data()
        print(f"User ID {user._user_id} registered successfully.")
        return True

    def borrow_book(self, isbn: str, user_id: str) -> bool:
        if isbn not in self._books or user_id not in self._users:
            print("Invalid ISBN or User ID.")
            return False

        book = self._books[isbn]
        user = self._users[user_id]

        if not book.borrow_book():
            print(f"Book with ISBN {isbn} is already borrowed.")
            return False

        due_date = datetime.today() + timedelta(days=BORROW_DAYS)
        user.add_borrowed_book(isbn, due_date)
        self._save_data()
        print(f"Book borrowed. Due date: {due_date.strftime('%Y-%m-%d')}")
        return True

    def return_book(self, isbn: str, user_id: str) -> bool:
        if isbn not in self._books or user_id not in self._users:
            print("Invalid ISBN or User ID.")
            return False

        user = self._users[user_id]
        book = self._books[isbn]

        if isbn not in user._borrowed_books:
            print("Book was not borrowed by this user.")
            return False

        due_str = user._borrowed_books[isbn]
        due_date = datetime.strptime(due_str, '%Y-%m-%d')
        today = datetime.today()
        late_days = (today - due_date).days

        if late_days > 0:
            fine = late_days * LATE_FEE_PER_DAY
            print(f"Book is {late_days} day(s) late. Fine: ₹{fine}")
        else:
            print("Book returned on time. No fine.")

        user.remove_borrowed_book(isbn)
        book.return_book()
        self._save_data()
        return True

    def search_book(self, query: str) -> List[Book]:
        query_lower = query.lower()
        return [book for book in self._books.values()
                if query_lower in book._title.lower()
                or query_lower in book._author.lower()
                or query_lower in book._isbn]

    def display_all_books(self, show_available_only: bool = False) -> None:
        for book in self._books.values():
            if show_available_only and book.get_status() != "Available":
                continue
            print(book)
            print("-" * 30)

    def display_all_users(self) -> None:
        for user in self._users.values():
            print(user)
            print("-" * 30)

    def display_user_borrowed_books(self, user_id: str) -> None:
        user = self._users.get(user_id)
        if not user:
            print("User not found.")
            return
        for isbn in user._borrowed_books:
            book = self._books.get(isbn)
            print(book)
            print(f"Due Date: {user._borrowed_books[isbn]}")
            print("-" * 30)

    def get_all_borrowed_books(self) -> None:
        for book in self._books.values():
            if book.get_status() == "Borrowed":
                print(book)
                print("-" * 30)

    def get_overdue_users(self) -> None:
        today = datetime.today()
        found = False
        for user in self._users.values():
            overdues = []
            for isbn, due_str in user._borrowed_books.items():
                due_date = datetime.strptime(due_str, '%Y-%m-%d')
                if today > due_date:
                    late_days = (today - due_date).days
                    fine = late_days * LATE_FEE_PER_DAY
                    book = self._books.get(isbn)
                    overdues.append((book, due_date, late_days, fine))
            if overdues:
                found = True
                print(f"User: {user._name} (ID: {user._user_id}) has overdue books:")
                for book, due_date, late_days, fine in overdues:
                    print(f"  - {book._title}, Due: {due_date.strftime('%Y-%m-%d')}, Late: {late_days} day(s), Fine: ₹{fine}")
                print("-" * 40)
        if not found:
            print("No users have overdue books.")

    def run(self):
        while True:
            print("\nLibrary Menu:")
            print("1. Add Book")
            print("2. Register User")
            print("3. Borrow Book")
            print("4. Return Book")
            print("5. Display All Books")
            print("6. Search Book")
            print("7. Display All Users")
            print("8. Display User's Borrowed Books")
            print("9. Display All Borrowed Books")
            print("10. Show Users With Overdue Books")
            print("11. Exit")
            choice = input("Enter your choice (1-11): ")

            if choice == '1':
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                isbn = input("Enter book ISBN: ")
                self.add_book(Book(title, author, isbn))

            elif choice == '2':
                name = input("Enter user name: ")
                user_id = input("Enter user ID: ")
                self.register_user(User(name, user_id))

            elif choice == '3':
                isbn = input("Enter ISBN of the book to borrow: ")
                user_id = input("Enter your user ID: ")
                self.borrow_book(isbn, user_id)

            elif choice == '4':
                isbn = input("Enter ISBN of the book to return: ")
                user_id = input("Enter your user ID: ")
                self.return_book(isbn, user_id)

            elif choice == '5':
                only_available = input("Show only available books? (y/n): ").strip().lower() == 'y'
                self.display_all_books(show_available_only=only_available)

            elif choice == '6':
                query = input("Enter title/author/ISBN to search: ")
                results = self.search_book(query)
                if results:
                    for book in results:
                        print(book)
                        print("-" * 30)
                else:
                    print("No matching books found.")

            elif choice == '7':
                self.display_all_users()

            elif choice == '8':
                user_id = input("Enter user ID: ")
                self.display_user_borrowed_books(user_id)

            elif choice == '9':
                self.get_all_borrowed_books()

            elif choice == '10':
                self.get_overdue_users()

            elif choice == '11':
                print("Exiting the Library System. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 11.")

def main():
    library = Library()
    library.run()

main()
