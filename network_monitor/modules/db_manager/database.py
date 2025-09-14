# network_monitor/modules/db_manager/database.py
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "devices.db")

def init_db():
    """Inicializa la base de datos con las tablas necesarias."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT UNIQUE,
        hostname TEXT,
        mac TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER,
        username TEXT,
        password TEXT,
        FOREIGN KEY(device_id) REFERENCES devices(id)
    )
    """)

    conn.commit()
    conn.close()

def get_credentials(ip):
    """Devuelve credenciales de un dispositivo por IP."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.username, c.password
        FROM devices d
        JOIN credentials c ON d.id = c.device_id
        WHERE d.ip = ?
    """, (ip,))
    result = cursor.fetchone()
    conn.close()

    return result if result else None

def save_device_and_credentials(ip, hostname, mac, username, password):
    """Guarda dispositivo y credenciales en la DB."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insertar o ignorar el dispositivo
    cursor.execute("""
        INSERT OR IGNORE INTO devices (ip, hostname, mac) VALUES (?, ?, ?)
    """, (ip, hostname, mac))

    # Obtener ID del dispositivo
    cursor.execute("SELECT id FROM devices WHERE ip = ?", (ip,))
    device_id = cursor.fetchone()[0]

    # Insertar credenciales
    cursor.execute("""
        INSERT INTO credentials (device_id, username, password)
        VALUES (?, ?, ?)
    """, (device_id, username, password))

    conn.commit()
    conn.close()
