# Netmiko/scripts/reset_db.py
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "../modules/database/net_devices.db")

def reset_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Borrar tablas si existen
    cursor.execute("DROP TABLE IF EXISTS lldp_neighbors")
    cursor.execute("DROP TABLE IF EXISTS credentials")
    cursor.execute("DROP TABLE IF EXISTS devices")

    # Crear tabla devices
    cursor.execute("""
    CREATE TABLE devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        type TEXT,
        ip TEXT,
        mac TEXT,
        model TEXT,
        location TEXT,
        registered_at TIMESTAMP
    )
    """)

    # Crear tabla credentials
    cursor.execute("""
    CREATE TABLE credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER,
        username TEXT,
        password TEXT
    )
    """)

    # Crear tabla lldp_neighbors
    cursor.execute("""
    CREATE TABLE lldp_neighbors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER,
        local_interface TEXT,
        neighbor_name TEXT,
        neighbor_port TEXT,
        neighbor_ip TEXT,
        neighbor_type TEXT,
        neighbor_model TEXT,
        last_seen TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos reiniciada y tablas creadas correctamente.")

if __name__ == "__main__":
    reset_db()
