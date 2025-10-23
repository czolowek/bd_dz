import sqlite3
from typing import Optional, List, Tuple

DB_PATH = "school_system.db"

def _connect():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db() -> None:
    conn = _connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS school (
        school_number INTEGER PRIMARY KEY,
        school_name TEXT NOT NULL,
        school_address TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS class (
        class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        school_number INTEGER,
        class_name TEXT NOT NULL,
        location TEXT,
        FOREIGN KEY (school_number) REFERENCES school(school_number)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS person (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        school_number INTEGER,
        address TEXT,
        class_number INTEGER,
        FOREIGN KEY (school_number) REFERENCES school(school_number),
        FOREIGN KEY (class_number) REFERENCES class(class_id)
    );
    """)


    cur.execute("SELECT 1 FROM school WHERE school_number = 12;")
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO school (school_number, school_name, school_address) VALUES (?, ?, ?);",
            (12, "Лицей №12", "ул. Школьная, 5")
        )


    cur.execute("SELECT 1 FROM class WHERE school_number = ? AND class_name = ?;", (12, "10-А"))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO class (school_number, class_name, location) VALUES (?, ?, ?);",
            (12, "10-А", "2 этаж, каб. 23")
        )

    conn.commit()
    conn.close()

def add_person(first_name: str, last_name: str, school_number: Optional[int], class_number: Optional[int], address: Optional[str]) -> None:
    conn = _connect()
    cur = conn.cursor()

    try:
        sn = int(school_number) if school_number not in (None, "", "None") else None
    except Exception:
        sn = None
    try:
        cn = int(class_number) if class_number not in (None, "", "None") else None
    except Exception:
        cn = None

    cur.execute(
        "INSERT INTO person (first_name, last_name, school_number, address, class_number) VALUES (?, ?, ?, ?, ?);",
        (first_name, last_name, sn, address, cn)
    )
    conn.commit()
    conn.close()

def get_people() -> List[Tuple]:
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT id, first_name, last_name, school_number, class_number, address FROM person ORDER BY id;")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_schools() -> List[Tuple]:
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT school_number, school_name, school_address FROM school ORDER BY school_number;")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_classes() -> List[Tuple]:
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT class_id, school_number, class_name, location FROM class ORDER BY class_id;")
    rows = cur.fetchall()
    conn.close()
    return rows
