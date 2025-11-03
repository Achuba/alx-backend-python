#!/usr/bin/python3
"""
4-stream_ages.py

Compute average age of users in a memory-efficient way
using a generator to stream ages one by one.
"""

import seed


def stream_user_ages():
    """
    Generator that yields user ages one by one from user_data table.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data;")

    for row in cursor:  # Only one loop
        yield row["age"]

    cursor.close()
    connection.close()


def compute_average_age():
    """
    Computes average age using the generator without loading all ages into memory.
    """
    total = 0
    count = 0

    for age in stream_user_ages():  # Second loop
        total += age
        count += 1

    if count == 0:
        average = 0
    else:
        average = total / count

    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    compute_average_age()
