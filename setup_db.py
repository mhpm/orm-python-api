import os
import sqlite3


# Connect to the SQLite database (creates the database if it doesn't exist)
def get_db_connection():
    db_path = os.path.join(os.getcwd(), "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


conn = get_db_connection()
# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    avatar TEXT
)
"""
)

# Initial list of 10 users
users = [
    (
        "John",
        "Doe",
        "john@example.com",
        "scrypt:32768:8:1$JEM9CYUgAciYtGds$f67d02727f7ce8af533c856f6c901ae77eaef9a486e3f747c4e68597d4a89d5d20c12e8cde8bf56f67b16b7e1d55ee966e3de17d985ea80f16321dcbaa72ae6f",
        "https://via.placeholder.com/150/0000FF/808080?Text=JohnDoe",
    ),
    (
        "Jane",
        "Smith",
        "jane@example.com",
        "scrypt:32768:8:1$JEM9CYUgAciYtGds$f67d02727f7ce8af533c856f6c901ae77eaef9a486e3f747c4e68597d4a89d5d20c12e8cde8bf56f67b16b7e1d55ee966e3de17d985ea80f16321dcbaa72ae6f",
        "https://via.placeholder.com/150/FF0000/FFFFFF?Text=JaneSmith",
    ),
    (
        "Alice",
        "Wonder",
        "alice@example.com",
        "scrypt:32768:8:1$JEM9CYUgAciYtGds$f67d02727f7ce8af533c856f6c901ae77eaef9a486e3f747c4e68597d4a89d5d20c12e8cde8bf56f67b16b7e1d55ee966e3de17d985ea80f16321dcbaa72ae6f",
        "https://via.placeholder.com/150/FFFF00/000000?Text=AliceWonder",
    ),
    (
        "Bob",
        "Builder",
        "bob@example.com",
        "scrypt:32768:8:1$JEM9CYUgAciYtGds$f67d02727f7ce8af533c856f6c901ae77eaef9a486e3f747c4e68597d4a89d5d20c12e8cde8bf56f67b16b7e1d55ee966e3de17d985ea80f16321dcbaa72ae6f",
        "https://via.placeholder.com/150/008000/FFFFFF?Text=BobBuilder",
    ),
    (
        "Charlie",
        "Chap",
        "charlie@example.com",
        "scrypt:32768:8:1$JEM9CYUgAciYtGds$f67d02727f7ce8af533c856f6c901ae77eaef9a486e3f747c4e68597d4a89d5d20c12e8cde8bf56f67b16b7e1d55ee966e3de17d985ea80f16321dcbaa72ae6f",
        "https://via.placeholder.com/150/000000/FFFFFF?Text=CharlieChap",
    ),
    (
        "Dana",
        "Scully",
        "dana@example.com",
        "scrypt:32768:8:1$JEM9CYUgAciYtGds$f67d02727f7ce8af533c856f6c901ae77eaef9a486e3f747c4e68597d4a89d5d20c12e8cde8bf56f67b16b7e1d55ee966e3de17d985ea80f16321dcbaa72ae6f",
        "https://via.placeholder.com/150/FF00FF/000000?Text=DanaScully",
    ),
    (
        "Edward",
        "Snow",
        "edward@example.com",
        "scrypt:32768:8:1$JEM9CYUgAciYtGds$f67d02727f7ce8af533c856f6c901ae77eaef9a486e3f747c4e68597d4a89d5d20c12e8cde8bf56f67b16b7e1d55ee966e3de17d985ea80f16321dcbaa72ae6f",
        "https://via.placeholder.com/150/800080/FFFFFF?Text=EdwardSnow",
    ),
    (
        "Fiona",
        "Sharp",
        "fiona@example.com",
        "scrypt:32768:8:1$JEM9CYUgAciYtGds$f67d02727f7ce8af533c856f6c901ae77eaef9a486e3f747c4e68597d4a89d5d20c12e8cde8bf56f67b16b7e1d55ee966e3de17d985ea80f16321dcbaa72ae6f",
        "https://via.placeholder.com/150/008080/FFFFFF?Text=FionaSharp",
    ),
    (
        "George",
        "Clay",
        "george@example.com",
        "scrypt:32768:8:1$JEM9CYUgAciYtGds$f67d02727f7ce8af533c856f6c901ae77eaef9a486e3f747c4e68597d4a89d5d20c12e8cde8bf56f67b16b7e1d55ee966e3de17d985ea80f16321dcbaa72ae6f",
        "https://via.placeholder.com/150/FFA500/FFFFFF?Text=GeorgeClay",
    ),
    (
        "Hannah",
        "Lee",
        "hannah@example.com",
        "scrypt:32768:8:1$JEM9CYUgAciYtGds$f67d02727f7ce8af533c856f6c901ae77eaef9a486e3f747c4e68597d4a89d5d20c12e8cde8bf56f67b16b7e1d55ee966e3de17d985ea80f16321dcbaa72ae6f",
        "https://via.placeholder.com/150/800000/FFFFFF?Text=HannahLee",
    ),
]

# Insert the users into the table
cursor.executemany(
    """
    INSERT INTO users (first_name, last_name, email, password, avatar) 
    VALUES (?, ?, ?, ?, ?)
""",
    users,
)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Database initialized with 10 users.")
