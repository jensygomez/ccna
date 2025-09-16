# NetMonDB/core/db_manager/db.py

import sqlite3

def init_db():
    conn = sqlite3.connect("NetMonDB.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hostname TEXT,
        running_config TEXT
    )
    """)
    conn.commit()
    return conn

def insert_or_update_device(conn, parsed_data):
    cursor = conn.cursor()
    # Ejemplo simple: siempre inserta
    cursor.execute("""
    INSERT INTO devices (hostname, running_config)
    VALUES (?, ?)
    """, ("Dispositivo1", parsed_data.get("show_running_config")))
    conn.commit()
