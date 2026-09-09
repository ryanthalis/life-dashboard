import sqlite3
from contextlib import contextmanager
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "life.db"


@contextmanager
def get_conn():
    db_connection = sqlite3.connect(FILE_PATH)
    db_connection.row_factory = sqlite3.Row

    try:
        with db_connection:
            yield db_connection
    finally:
        db_connection.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date TEXT NOT NULL CONSTRAINT valid_date CHECK (entry_date IS date(entry_date)),
                category TEXT NOT NULL CHECK(category IN ('workout', 'study')),
                label TEXT NOT NULL CHECK(trim(label) != ''),
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                notes TEXT
            )STRICT;
        """)

        user_version = conn.execute("PRAGMA user_version").fetchone()[0]

        if user_version == 0:
            migrate_v0_to_v1(conn)



def add_entry(entry_date: str, category: str, label: str, quantity: int, notes: str = ""):

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO entries (entry_date, category, label, quantity, notes)
            VALUES (?, ?, ?, ?, ?);
        """, (entry_date, category, label, quantity, notes))


def get_entries(category: str | None = None):

    data = []

    if category is None:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT
                                *
                                FROM
                                    entries
                                ORDER BY
                                    entry_date DESC, 
                                    id DESC
                                """)
            data = cursor.fetchall()


    elif category in ("workout", "study"):

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


def update_entry(entry_id: int, entry_date: str, category: str, label: str, quantity: int, notes: str = "",) -> bool:
    with get_conn() as conn:
        cursor = conn.execute(
            """
            UPDATE entries
            SET
                entry_date = ?,
                category = ?,
                label = ?,
                quantity = ?,
                notes = ?
            WHERE id = ?
            """,
            (entry_date, category, label, quantity, notes, entry_id),
        )
        return cursor.rowcount == 1

def delete_entry(entry_id: int) -> bool:

    with get_conn() as conn:
        cursor = conn.execute(
            """
            DELETE FROM entries
            WHERE id = ?
            """,
            (entry_id,),
        )
        
        return cursor.rowcount == 1



def get_entry(entry_id: int) -> sqlite3.Row | None:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT
                id,
                entry_date,
                category,
                label,
                quantity,
                notes
            FROM entries
            WHERE id = ?
            """,
            (entry_id,),
        ).fetchone()

def migrate_v0_to_v1(conn: sqlite3.Connection):

    conn.execute("""ALTER TABLE entries RENAME TO entries_old;
    """)
    conn.execute("""CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date TEXT NOT NULL CONSTRAINT valid_date CHECK (entry_date IS date(entry_date)),
                category TEXT NOT NULL CHECK(category IN ('workout', 'study')),
                label TEXT NOT NULL CHECK(trim(label) != ''),
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                notes TEXT
            )STRICT;
        """)
    
    conn.execute("""INSERT INTO entries (id, entry_date, category, label, quantity, notes)
                SELECT id, entry_date, category, label, quantity, notes
                FROM entries_old
                """)
    
    conn.execute("""DROP TABLE entries_old;""")

    conn.execute("PRAGMA user_version = 1")
