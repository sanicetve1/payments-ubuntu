# db.py
import sqlite3
from app.config import DB_PATH

def query_db(query: str, params: tuple = (), one: bool = False):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return dict(rows[0]) if one and rows else [dict(row) for row in rows]
