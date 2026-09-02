import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "life.db" 


def get_conn():
    db_connection = sqlite3.connect(FILE_PATH)
    db_connection.row_factory = sqlite3.Row
    return db_connection

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date TEXT NOT NULL,
                category TEXT NOT NULL,
                label TEXT NOT NULL,
                quantity INTEGER,
                notes TEXT
            );
        """)


def add_entry(entry_date: str, category: str, label: str, quantity: int | None, notes: str = ""):

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO entries (entry_date, category, label, quantity, notes)
            VALUES (?, ?, ?, ?, ?);
        """, (entry_date, category, label, quantity, notes))


def get_entries(category: str):

    data = []

    if category in ("workout", "study"):

        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT
                                id,
                                entry_date,
                                category,
                                label,
                                quantity,
                                notes
                            FROM 
                                entries
                            WHERE category = ? 
                            ORDER BY
                                entry_date DESC, 
                                id DESC
                        """, (category,))
            
            data = cursor.fetchall()
    else:
        raise ValueError("category must be workout or study")

    return data

if __name__ == "__main__":
    init_db()
    data = get_entries("workout")
    for i in data:
        print(i["id"])
        print(i["entry_date"])
        print(i["category"])
        print(i["label"])
        print(i["quantity"])
        print(i["notes"])

        