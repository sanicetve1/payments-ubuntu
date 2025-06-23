# agent/memory.py

import sqlite3
from agents.state import AgentState
import os

# Define your agent memory DB file
DB_FILE = os.path.join(os.path.dirname(__file__), "agent_memory.db")

def init_memory_db():
    """Initializes the SQLite DB to store conversation state."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            state_json TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_state(state: AgentState):
    """Persists a serialized AgentState into SQLite."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT OR REPLACE INTO memory (id, timestamp, state_json) VALUES (?, ?, ?)",
        (state.conversation_id, state.timestamp, state.serialize())
    )
    conn.commit()
    conn.close()

def load_state(conversation_id: str) -> AgentState:
    """Fetches a stored state by conversation ID."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT state_json FROM memory WHERE id = ?", (conversation_id,))
    row = cur.fetchone()
    conn.close()
    return AgentState.deserialize(row[0]) if row else None

def list_conversations(limit: int = 10) -> list:
    """Returns summaries of recent conversations for debug/UI."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, timestamp, state_json FROM memory ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()

    summaries = []
    for row in rows:
        state = AgentState.deserialize(row[2])
        summaries.append(state.summary())
    return summaries
