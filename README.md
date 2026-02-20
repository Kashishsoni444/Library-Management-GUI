# Library-Management-GUI
Rebuilt a terminal-based Python library management system into a full desktop GUI application using Tkinter. Features a live dashboard with real-time stats, tabbed navigation for book and member management, and an issue/return tracking system — all connected to a MySQL database.


# 📚 Library Management System — GUI Edition

A desktop application for managing a library's books, members, and book issues/returns. Built with Python and Tkinter, connected to a MySQL database. Converted from a terminal-based CLI project into a fully featured graphical interface.

---

## ✨ Features

- **Dashboard** — Live stats for total books, members, active issues, and returns today
- **Book Management** — Add, search, update, and delete book records
- **Member Management** — Add, search, update, and delete library members
- **Issue & Return** — Issue books to members and log returns with today's date auto-filled
- **Results Table** — All search results displayed in a clean, scrollable table
- **Toast Notifications** — Non-intrusive success/error popups instead of terminal output
- **Dark Theme UI** — Easy on the eyes for extended use

---

## 🗂️ Project Structure

```
├── library_management_gui.py   # Main application (GUI)
├── library_management.py       # Original CLI version
└── README.md
```

---

## 🛠️ Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Language   | Python 3.x              |
| GUI        | Tkinter (built-in)      |
| Database   | MySQL                   |
| DB Driver  | mysql-connector-python  |

---

## ⚙️ Database Setup

Make sure you have MySQL installed and running. Create the database and tables before launching the app.

```sql
CREATE DATABASE Library;

USE Library;

CREATE TABLE BOOKRECORDS (
    bno               INT PRIMARY KEY,
    bname             VARCHAR(100),
    auth              VARCHAR(100),
    price             INT,
    publ              VARCHAR(100),
    qty               INT,
    date_of_purchase  DATE
);

CREATE TABLE MEMBER (
    mno                  VARCHAR(20) PRIMARY KEY,
    mname                VARCHAR(100),
    date_of_membership   DATE,
    addr                 VARCHAR(200),
    mob                  VARCHAR(15)
);

CREATE TABLE ISSUE (
    bno         INT,
    mno         VARCHAR(20),
    d_o_issue   DATE,
    d_o_ret     DATE DEFAULT NULL
);
```

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install mysql-connector-python
```

> Tkinter comes pre-installed with Python. No extra install needed.

### 2. Configure your database credentials

Open `library_management_gui.py` and update the `DB_CONFIG` at the top of the file:

```python
DB_CONFIG = dict(
    user="root",
    host="localhost",
    passwd="your_password",
    database="Library"
)
```

### 3. Run the app

```bash
python library_management_gui.py
```

---

## 🧭 How to Use

### Dashboard
- Opens automatically on launch
- Click **Refresh Dashboard** to pull the latest stats from the database

### Books
- Fill in all fields and click **Add Book** to insert a new record
- Enter a Book Code and click **Delete Book** to remove it (confirmation required)
- Enter a Book Code in the search box and click **Search** to look up a book
- After searching, fill in the form fields and click **Update** to modify the record

### Members
- Works the same way as the Books tab — Add, Delete, Search, Update

### Issue / Return
- Fill in Book Code, Member Code, and Issue Date, then click **Issue Book**
- To return a book, enter the Book Code and Member Code and click **Return Book** — today's date is auto-filled as the return date
- Search all issues for a member using their Member Code

---

## 📦 Requirements

```
Python >= 3.7
mysql-connector-python
MySQL Server
```

---

## 🔄 Changelog

| Version | Notes |
|---------|-------|
| 2.0 | Full GUI rewrite using Tkinter — tabbed layout, dark theme, live dashboard |
| 1.0 | Original CLI version using terminal menus |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
