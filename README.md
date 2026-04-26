# 📚 Library Management System (Python + MySQL)
A CLI-based Library Management System built with Python and MySQL. It supports book management, issuer registration, issuing and returning books, and tracking records. Ensures data integrity using SQL constraints and handles real-world scenarios like stock updates and restricted deletions.

A fully functional **Library Management System (LMS)** built using **Python** and **MySQL**, designed to handle core library operations through a simple command-line interface.

---

## 📖 Overview
This project allows users to efficiently manage books, issuers, and book transactions. It includes features such as:
- Adding, updating, and deleting books  
- Registering users (issuers)  
- Issuing and returning books  
- Tracking issued records with return status  

The system ensures **data integrity** using MySQL constraints like **primary keys, foreign keys, and unique fields**. It also handles real-world scenarios such as preventing deletion of issued books and managing stock availability.

---

## 🔑 Key Features
- 📘 Add, update, delete, and view books  
- 👤 Register and manage issuers  
- 🔄 Issue and return books with due date tracking  
- 📊 Automatic stock updates on issue/return  
- 🔒 Prevent deletion of books currently issued  
- 🧩 MySQL database integration with relational structure  

---

## 🛠️ Tech Stack
- **Python** (CLI-based application)  
- **MySQL** (Database)  
- **mysql-connector-python** (Database connector)  

---

## ⚙️ Setup Instructions

### 1. Install Dependencies
```bash
pip install mysql-connector-python
```
### 2. Create Database
Run the following SQL command in MySQL:
```sql
CREATE DATABASE lms2026;
```
