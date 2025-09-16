# NetMonDB/core/db_manager/db.py

# core/db_manager/db.py
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "net_devices.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hostname TEXT,
        ip TEXT,
        username TEXT,
        password TEXT,
        gateway TEXT,
        interface TEXT,
        device_type TEXT,
        last_update TEXT,
        running_config TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_or_update_device(device_info, parsed_data=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Usar defaults si algunas claves no existen
    device_type = device_info.get('device_type', 'cisco_ios')
    gateway = device_info.get('gateway', '')
    interface = device_info.get('interface', '')
    last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    running_config = str(parsed_data) if parsed_data else ""

    # Verificar si ya existe el dispositivo
    cursor.execute("SELECT id FROM devices WHERE hostname = ?", (device_info['hostname'],))
    result = cursor.fetchone()

    if result:
        cursor.execute("""
            UPDATE devices SET
            ip = ?, username = ?, password = ?, gateway = ?, interface = ?,
            device_type = ?, last_update = ?, running_config = ?
            WHERE id = ?
        """, (
            device_info['ip'],
            device_info['username'],
            device_info['password'],
            gateway,
            interface,
            device_type,
            last_update,
            running_config,
            result[0]
        ))
    else:
        cursor.execute("""
            INSERT INTO devices (hostname, ip, username, password, gateway, interface, device_type, last_update, running_config)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            device_info['hostname'],
            device_info['ip'],
            device_info['username'],
            device_info['password'],
            gateway,
            interface,
            device_type,
            last_update,
            running_config
        ))

    conn.commit()
    conn.close()

def get_all_devices():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()
    conn.close()
    return devices
