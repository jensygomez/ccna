# Netmiko/modules/database_manager/db_utils.py
import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "net_devices.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Crear tabla devices
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
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
    CREATE TABLE IF NOT EXISTS credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER,
        username TEXT,
        password TEXT
    )
    """)
    # Crear tabla lldp_neighbors
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lldp_neighbors (
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

# --------- Bastion ---------
def get_bastion_credentials():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.ip, c.username, c.password, d.id
        FROM devices d
        JOIN credentials c ON c.device_id = d.id
        WHERE d.name='Bastion'
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"host": row[0], "username": row[1], "password": row[2], "device_id": row[3], "secret": row[2]}
    return None

def add_or_update_bastion(host, username, password, name="Bastion"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Verificar si ya existe
    cursor.execute("SELECT id FROM devices WHERE name=?", (name,))
    row = cursor.fetchone()
    if row:
        device_id = row[0]
        # Actualizar IP si cambió
        cursor.execute("UPDATE devices SET ip=?, registered_at=? WHERE id=?", 
                       (host, datetime.now(), device_id))
        cursor.execute("UPDATE credentials SET username=?, password=? WHERE device_id=?",
                       (username, password, device_id))
    else:
        cursor.execute("INSERT INTO devices (name, ip, registered_at) VALUES (?, ?, ?)",
                       (name, host, datetime.now()))
        device_id = cursor.lastrowid
        cursor.execute("INSERT INTO credentials (device_id, username, password) VALUES (?, ?, ?)",
                       (device_id, username, password))
    conn.commit()
    conn.close()
    return device_id

# --------- Devices ---------
def add_or_update_device(name, type_, ip=None, mac=None, model=None, location=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM devices WHERE mac=? OR ip=?", (mac, ip))
    row = cursor.fetchone()
    if row:
        device_id = row[0]
        cursor.execute("""
            UPDATE devices SET name=?, type=?, model=?, location=?, registered_at=?
            WHERE id=?
        """, (name, type_, model, location, datetime.now(), device_id))
    else:
        cursor.execute("""
            INSERT INTO devices (name, type, ip, mac, model, location, registered_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, type_, ip, mac, model, location, datetime.now()))
        device_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return device_id

def get_devices():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices")
    rows = cursor.fetchall()
    conn.close()
    return rows

# --------- LLDP Neighbors ---------
def add_or_update_lldp_neighbor(device_id, local_interface, neighbor_name, neighbor_port,
                                neighbor_ip=None, neighbor_type=None, neighbor_model=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Verificar si ya existe un vecino idéntico
    cursor.execute("""
        SELECT id FROM lldp_neighbors
        WHERE device_id=? AND local_interface=? AND neighbor_name=?
    """, (device_id, local_interface, neighbor_name))
    row = cursor.fetchone()
    if row:
        neighbor_id = row[0]
        cursor.execute("""
            UPDATE lldp_neighbors
            SET neighbor_port=?, neighbor_ip=?, neighbor_type=?, neighbor_model=?, last_seen=?
            WHERE id=?
        """, (neighbor_port, neighbor_ip, neighbor_type, neighbor_model, datetime.now(), neighbor_id))
    else:
        cursor.execute("""
            INSERT INTO lldp_neighbors (device_id, local_interface, neighbor_name, neighbor_port,
                                        neighbor_ip, neighbor_type, neighbor_model, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (device_id, local_interface, neighbor_name, neighbor_port,
              neighbor_ip, neighbor_type, neighbor_model, datetime.now()))
    conn.commit()
    conn.close()