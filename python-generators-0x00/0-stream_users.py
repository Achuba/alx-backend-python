#!/usr/bin/python3
"""
0-stream_users.py

Defines a generator function that streams rows one by one
from the `user_data` table in the ALX_prodev database.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Connects to the ALX_prodev database and yields rows one by one
    from the user_data table using a generator.

    Returns:
        generator: yields each row as a dictionary
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  # Update if your MySQL password differs
            database="ALX_prodev"
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            # Single loop for generator (per project requirement)
            for row in cursor:
                yield row

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error while streaming users: {e}")
        return
