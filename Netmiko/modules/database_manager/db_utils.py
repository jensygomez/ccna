# Netmiko/modules/database_manager/db_utils.py
import sqlite3
import os
from datetime import datetime

# ------------------------------
# Rutas de la base de datos
# ------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FOLDER = os.path.join(BASE_DIR, "database")
os.makedirs(DB_FOLDER, exist_ok=True)
DB_PATH = os.path.join(DB_FOLDER, "net_devices.db")


# ------------------------------
# Inicialización de la DB
# ------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla de dispositivos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        ip TEXT NOT NULL UNIQUE,
        mac TEXT UNIQUE,
        model TEXT,
        location TEXT,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Tabla de interfaces
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interfaces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        mac TEXT,
        ip TEXT,
        status TEXT,
        description TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
    )
    """)

    # Tabla de credenciales
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
    )
    """)

    # Tabla de logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        command TEXT,
        output TEXT,
        executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH}")


# ------------------------------
# Funciones CRUD y sync
# ------------------------------
def add_or_update_device(name, type_, ip, mac=None, model=None, location=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, mac FROM devices WHERE ip = ?", (ip,))
    row = cursor.fetchone()
    if row:
        device_id, old_mac = row
        if mac and mac != old_mac:
            cursor.execute("UPDATE devices SET mac = ? WHERE id = ?", (mac, device_id))
        conn.commit()
    else:
        cursor.execute("""
            INSERT INTO devices (name, type, ip, mac, model, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, type_, ip, mac, model, location))
        device_id = cursor.lastrowid
        conn.commit()
    conn.close()
    return device_id


def add_or_update_interface(device_id, name, mac=None, ip=None, status=None, description=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, mac, ip, status, description FROM interfaces
        WHERE device_id = ? AND name = ?
    """, (device_id, name))
    row = cursor.fetchone()
    if row:
        interface_id, old_mac, old_ip, old_status, old_desc = row
        cursor.execute("""
            UPDATE interfaces
            SET mac = ?, ip = ?, status = ?, description = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (mac or old_mac, ip or old_ip, status or old_status, description or old_desc, interface_id))
    else:
        cursor.execute("""
            INSERT INTO interfaces (device_id, name, mac, ip, status, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (device_id, name, mac, ip, status, description))
    conn.commit()
    conn.close()


def add_interface(device_id, name, mac=None, ip=None, status=None, description=None):
    """ Función de compatibilidad antigua """
    add_or_update_interface(device_id, name, mac, ip, status, description)


def add_device(name, type_, ip, mac=None, model=None, location=None):
    """ Función de compatibilidad antigua """
    return add_or_update_device(name, type_, ip, mac, model, location)


def sync_device_interfaces(device_id, interfaces):
    """
    interfaces = [
        {"name": "GigabitEthernet0/0", "mac": "aa:bb:cc:dd:ee:ff", "ip": "192.168.18.110",
         "status": "up", "description": "To Home LAN"},
        ...
    ]
    """
    for intf in interfaces:
        add_or_update_interface(
            device_id,
            name=intf.get("name"),
            mac=intf.get("mac"),
            ip=intf.get("ip"),
            status=intf.get("status"),
            description=intf.get("description")
        )


def add_log(device_id, command, output):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (device_id, command, output)
        VALUES (?, ?, ?)
    """, (device_id, command, output))
    conn.commit()
    conn.close()


def get_devices():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, ip FROM devices")
    devices = cursor.fetchall()
    conn.close()
    return devices
def get_last_log_for_interface(device_id, interface_name):
    """
    Retorna el último Output registrado en logs para un dispositivo y una interfaz.
    Si no hay logs previos, retorna None.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT output 
        FROM logs 
        WHERE device_id = ? AND command = ?
        ORDER BY executed_at DESC
        LIMIT 1
    """, (device_id, f"Sync {interface_name}"))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return row[0]
    return None


# ------------------------------
# Inicialización si se ejecuta directamente
# ------------------------------
if __name__ == "__main__":
    init_db()
