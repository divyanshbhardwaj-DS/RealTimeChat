import sqlite3
from pathlib import Path

# Create database folder if it doesn't exist
Path("database").mkdir(exist_ok=True)

DB_PATH = "database/chat.db"


def connect():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = connect()
    cursor = conn.cursor()
#User Table
    cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP,
    status TEXT DEFAULT 'Offline'
)
""")

    # Messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("✅ Database Initialized Successfully")


if __name__ == "__main__":
    initialize_database()