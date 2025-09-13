#Netmiko/core/sync.pyimport sqlite3
from datetime import datetime

DB_PATH = "modules/database/net_devices.db"

def sync_devices_to_db(devices):
    """
    Sincroniza dispositivos descubiertos con la base de datos.
    devices = [{"ip": "192.168.0.1", "name": "DeviceX", "type": "Router"}]
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        type TEXT,
        ip TEXT UNIQUE,
        mac TEXT,
        model TEXT,
        location TEXT,
        registered TIMESTAMP
    )
    """)

    for dev in devices:
        cursor.execute("""
        INSERT INTO devices (name, type, ip, mac, model, location, registered)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(ip) DO UPDATE SET
            name=excluded.name,
            type=excluded.type,
            registered=excluded.registered
        """, (
            dev.get("name", "Unknown"),
            dev.get("type", "Unknown"),
            dev["ip"],
            dev.get("mac", "N/A"),
            dev.get("model", "N/A"),
            dev.get("location", "N/A"),
            datetime.now()
        ))

    conn.commit()
    conn.close()
