# 📚 Library Management System

A Python-based command-line Library Management System that enables users to manage books and members with ease. It supports borrowing and returning books, tracking due dates, and calculating overdue fines — all stored persistently using JSON files.

---

## 🔧 Features

- ➕ Add new books (Title, Author, ISBN)
- 👥 Register users (Name, User ID)
- 📚 Borrow books (14-day period)
- 📤 Return books and auto-calculate late fees (₹10 per day)
- 📆 Track due dates and overdue returns
- 🔍 Search books by title, author, or ISBN
- 📑 Display all or only available books
- 📄 View all registered users and their borrowed books
- 📋 View all borrowed books
- ❗ Identify users with overdue books and fines
- 💾 Persistent storage using `books.json` and `users.json`
- 📘 Single Python file for easy use and deployment

---

## 🏗️ Built With

- **Language**: Python  
- **Libraries Used**:
  - `json` – for data persistence
  - `datetime` – for date handling
  - `typing` – for type hinting

---

## 🚀 Getting Started

### 🔹 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/GitSetGoRishabh/Library-Management-System-Python.git
   cd Library-Management-System-Python

2. (Optional) Create a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate    # macOS/Linux
  venv\Scripts\activate       # Windows
  ```

3. Run the project:
  ```bash
  python library_management.py
  ```
The system will automatically generate books.json and users.json files for saving data.

## 📁 Project Structure
  ```bash
  Library-Management-System-Python/
  │
  ├── library_management.py   # All classes and logic in one file
  ├── books.json              # Auto-generated book data file
  ├── users.json              # Auto-generated user data file
  ├── LICENSE                 # License file (MIT)
  └── README.md               # Project documentation
  ```

## 📜 License
This project is licensed under the MIT License.
See the LICENSE file for details.


## 🌱 Future Enhancements
GUI version (Tkinter, PyQt)

Export data as CSV/PDF

Email reminders for overdue books

More detailed reports and analytics

## 👤 Author
Rishabh Singh Yadav

## 🙌 Contributing
Have an idea or found a bug?
Fork the repo and create a pull request — contributions are welcome!

## 📫 Contact
For questions, raise an issue on the repository.
