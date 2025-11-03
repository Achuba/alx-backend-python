#!/usr/bin/python3
"""
seed.py

This script sets up a MySQL database (ALX_prodev), creates a user_data table,
loads data from a CSV file, and includes a generator to stream rows
from the database one by one.
"""

import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """Connects to the MySQL server (no specific database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"  # Change this if your MySQL root password is different
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
        cursor.close()
        print("Database ALX_prodev created successfully (if not exists)")
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Creates the user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Inserts CSV data into the user_data table if it does not already exist."""
    try:
        cursor = connection.cursor()

        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if record already exists
                cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s;", (row['user_id'],))
                existing = cursor.fetchone()

                if not existing:
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s);
                    """, (
                        row['user_id'] if row['user_id'] else str(uuid.uuid4()),
                        row['name'],
                        row['email'],
                        row['age']
                    ))

        connection.commit()
        cursor.close()
        print("Data inserted successfully into user_data table")
    except Error as e:
        print(f"Error inserting data: {e}")


def stream_user_data(connection):
    """
    Generator function that streams rows from the user_data table one by one.
    """
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
        cursor.close()
    except Error as e:
        print(f"Error streaming data: {e}")
        return


if __name__ == "__main__":
    # Optional direct run for testing
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()
        conn = connect_to_prodev()
        if conn:
            create_table(conn)
            insert_data(conn, "user_data.csv")

            print("Streaming first 5 rows:")
            count = 0
            for row in stream_user_data(conn):
                print(row)
                count += 1
                if count >= 5:
                    break
            conn.close()
