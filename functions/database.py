import sqlite3, os
from typing import List, Dict


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'posts.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

