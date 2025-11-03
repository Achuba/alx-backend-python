#!/usr/bin/python3
"""
1-batch_processing.py

Fetches users in batches and processes them using generators.
"""

import mysql.connector
from mysql.connector import Error

# Generator to fetch rows in batches
def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of rows from user_data table.
    
    Args:
        batch_size (int): Number of rows per batch
    Yields:
        list[dict]: List of user dictionaries
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            offset = 0

            while True:
                cursor.execute(
                    "SELECT * FROM user_data LIMIT %s OFFSET %s;",
                    (batch_size, offset)
                )
                batch = cursor.fetchall()
                if not batch:
                    break
                yield batch
                offset += batch_size

            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error fetching users in batches: {e}")
        return


# Process batches to filter users over age 25
def batch_processing(batch_size):
    """
    Processes each batch to filter users over age 25.

    Args:
        batch_size (int): Number of rows per batch
    Yields:
        dict: User records where age > 25
    """
    for batch in stream_users_in_batches(batch_size):  # 1st loop
        for user in batch:  # 2nd loop
            if user["age"] > 25:  # Filtering
                print(user)  # or yield user if preferred
