import sqlite3

DB_PATH = "school_system.db"

def _connect():
    return sqlite3.connect(DB_PATH)

def init_db():
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


    cur.execute("""
    CREATE TABLE IF NOT EXISTS basket (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER DEFAULT 1
    );
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)


    cur.execute("INSERT OR IGNORE INTO school (school_number, school_name, school_address) VALUES (12, 'Лицей №12', 'ул. Школьная, 5');")
    cur.execute("INSERT OR IGNORE INTO class (class_id, school_number, class_name, location) VALUES (1, 12, '10-А', '2 этаж, каб. 23');")
    cur.execute("INSERT OR IGNORE INTO admin (admin_id, username, password) VALUES (1, 'admin', '12345');")
    cur.execute("INSERT OR IGNORE INTO basket (item_id, item_name, price, quantity) VALUES (1, 'Учебник по математике', 250.0, 3);")

    conn.commit()
    conn.close()

def add_person(first_name, last_name, school_number, class_number, address):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO person (first_name, last_name, school_number, class_number, address)
        VALUES (?, ?, ?, ?, ?);
    """, (first_name, last_name, school_number, class_number, address))
    conn.commit()
    conn.close()

def get_people():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT id, first_name, last_name, school_number, class_number, address FROM person;")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_schools():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM school;")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_classes():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM class;")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_basket():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM basket;")
    rows = cur.fetchall()
    conn.close()
    return rows



def sql_examples():
    conn = _connect()
    cur = conn.cursor()


    cur.execute("ALTER TABLE basket ADD COLUMN category TEXT DEFAULT 'учебники';")


    cur.execute("DELETE FROM basket WHERE quantity = 0;")


    cur.execute("SELECT COUNT(*) FROM person WHERE school_number = 12;")
    count = cur.fetchone()[0]


    cur.execute("SELECT MAX(price), MIN(price) FROM basket;")
    max_price, min_price = cur.fetchone()


    cur.execute("""
        SELECT first_name, last_name
        FROM person
        WHERE school_number = (
            SELECT school_number FROM school WHERE school_name = 'Лицей №12'
        );
    """)
    nested = cur.fetchall()


    cur.execute("""
        SELECT p.first_name, p.last_name, c.class_name
        FROM person p
        INNER JOIN class c ON p.class_number = c.class_id;
    """)
    inner = cur.fetchall()

    cur.execute("""
        SELECT s.school_name, c.class_name
        FROM school s
        LEFT OUTER JOIN class c ON s.school_number = c.school_number;
    """)
    outer = cur.fetchall()


    cur.execute("""
        SELECT first_name AS name FROM person
        UNION
        SELECT username AS name FROM admin;
    """)
    union = cur.fetchall()

    conn.commit()
    conn.close()

    return {
        "count": count,
        "max": max_price,
        "min": min_price,
        "nested": nested,
        "inner": inner,
        "outer": outer,
        "union": union
    }
