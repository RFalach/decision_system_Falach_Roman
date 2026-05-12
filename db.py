import sqlite3

DB_NAME = "swords.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS swords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS criteria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL DEFAULT 'maximize',
            weight REAL DEFAULT 0.0,
            unit TEXT DEFAULT ''
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sword_id INTEGER NOT NULL,
            criterion_id INTEGER NOT NULL,
            value REAL NOT NULL,
            FOREIGN KEY (sword_id) REFERENCES swords(id) ON DELETE CASCADE,
            FOREIGN KEY (criterion_id) REFERENCES criteria(id) ON DELETE CASCADE,
            UNIQUE(sword_id, criterion_id)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS expert_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expert_name TEXT NOT NULL,
            sword_id INTEGER NOT NULL,
            criterion_id INTEGER NOT NULL,
            rating REAL NOT NULL,
            FOREIGN KEY (sword_id) REFERENCES swords(id) ON DELETE CASCADE,
            FOREIGN KEY (criterion_id) REFERENCES criteria(id) ON DELETE CASCADE
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition TEXT NOT NULL,
            action TEXT NOT NULL,
            is_active INTEGER DEFAULT 1
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS voting_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method TEXT NOT NULL,
            criterion_id INTEGER NOT NULL,
            weight REAL NOT NULL,
            FOREIGN KEY (criterion_id) REFERENCES criteria(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()
