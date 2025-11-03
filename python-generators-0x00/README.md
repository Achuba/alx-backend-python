# Python Generators – Database Streaming

## 🎯 Objective
Create a generator that streams rows from an SQL database one by one using Python.

---

## 🧩 Description
This project sets up a **MySQL database (`ALX_prodev`)**, creates a **`user_data`** table, and loads sample data from a CSV file.  
It also includes a **generator function** that streams rows from the database **lazily**, without loading all data into memory.

---

## 📂 Files

| File | Description |
|------|--------------|
| `seed.py` | Contains all database setup, seeding, and streaming logic |
| `user_data.csv` | Sample user data file |
| `0-main.py` | Test script provided to verify setup and data loading |

---

## ⚙️ Functions

| Function | Description |
|-----------|--------------|
| `connect_db()` | Connects to the MySQL server |
| `create_database(connection)` | Creates the `ALX_prodev` database if it does not exist |
| `connect_to_prodev()` | Connects to the `ALX_prodev` database |
| `create_table(connection)` | Creates the `user_data` table |
| `insert_data(connection, data)` | Inserts records from `user_data.csv` |
| `stream_user_data(connection)` | **Generator** that yields rows one at a time |

---

## 🧠 Example Usage

```bash
$ ./0-main.py
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ...]
