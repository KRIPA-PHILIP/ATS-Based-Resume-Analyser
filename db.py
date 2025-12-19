import sqlite3
import pandas as pd
import os

DB_FILE = "data/ats.db"

def init_db():
    """Initializes the database file and candidate table."""
    if not os.path.exists("data"):
        os.makedirs("data")
        
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            score REAL,
            skills TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_candidate(name, score, skills):
    """Saves a new analysis result to the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO candidates (name, score, skills) VALUES (?, ?, ?)", 
              (name, score, str(skills)))
    conn.commit()
    conn.close()

def get_all_candidates():
    """Fetches all history for the dashboard."""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM candidates ORDER BY date DESC", conn)
    conn.close()
    return df