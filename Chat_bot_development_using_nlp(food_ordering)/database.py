import sqlite3

def init_db():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            items TEXT,
            total INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_user_data(name, phone, order):
    items = ", ".join([f"{item} ₹{price}" for item, price in order])
    total = sum([price for _, price in order])
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("INSERT INTO orders (name, phone, items, total) VALUES (?, ?, ?, ?)",
              (name, phone, items, total))
    conn.commit()
    conn.close()
