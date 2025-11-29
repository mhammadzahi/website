import sqlite3, os
# from typing import List, Dict


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'posts.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def new_subscriber(email: str) -> bool:
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO newsletter_subscribers (email) VALUES (?)", (email,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error adding subscriber:", e)
        return False

def new_message(name: str, email: str, subject: str, message: str) -> bool:
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO contact_messages (full_name, email_address, subject, message) VALUES (?, ?, ?, ?)",
                    (name, email, subject, message))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error saving contact message:", e)
        return False
