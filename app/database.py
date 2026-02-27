import sqlite3
import os

DB_DIR = "data"
DB_FILE = os.path.join(DB_DIR, "keys.db")

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY,
            provider TEXT UNIQUE NOT NULL,
            api_key TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_api_key(provider: str, api_key: str):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Insert or replace if the provider key already exists
    cursor.execute("""
        INSERT INTO api_keys (id, provider, api_key) 
        VALUES (1, ?, ?)
        ON CONFLICT(id) DO UPDATE SET api_key=excluded.api_key;
    """, (provider, api_key))
    conn.commit()
    conn.close()

def get_api_key(provider: str) -> str | None:
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT api_key FROM api_keys WHERE provider = ?", (provider,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    return None
