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

    # Tabla LLDP neighbors
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
        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
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
# Funciones CRUD
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


def add_or_update_lldp(device_id, local_intf, neighbor_name, neighbor_port=None,
                       neighbor_ip=None, neighbor_type=None, neighbor_model=None,
                       timestamp=None):
    """
    Agrega o actualiza un vecino LLDP con todos los campos.
    """
    timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM lldp_neighbors
        WHERE device_id=? AND local_interface=? AND neighbor_name=?
    """, (device_id, local_intf, neighbor_name))
    result = cursor.fetchone()

    if result:
        neighbor_id = result[0]
        cursor.execute("""
            UPDATE lldp_neighbors
            SET neighbor_port=?, neighbor_ip=?, neighbor_type=?, neighbor_model=?, last_seen=?
            WHERE id=?
        """, (neighbor_port, neighbor_ip, neighbor_type, neighbor_model, timestamp, neighbor_id))
    else:
        cursor.execute("""
            INSERT INTO lldp_neighbors 
            (device_id, local_interface, neighbor_name, neighbor_port, neighbor_ip, neighbor_type, neighbor_model, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (device_id, local_intf, neighbor_name, neighbor_port, neighbor_ip, neighbor_type, neighbor_model, timestamp))

    conn.commit()
    conn.close()


def add_log(device_id, command, output):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (device_id, command, output)
        VALUES (?, ?, ?)
    """, (device_id, command, output))
    conn.commit()
    conn.close()


def get_last_log_for_interface(device_id, interface_name):
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
    return row[0] if row else None


def add_credentials(device_id, username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO credentials (device_id, username, password)
        VALUES (?, ?, ?)
    """, (device_id, username, password))
    conn.commit()
    conn.close()


def get_devices():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, ip FROM devices")
    devices = cursor.fetchall()
    conn.close()
    return devices


def sync_device_interfaces(device_id, interfaces):
    for intf in interfaces:
        add_or_update_interface(
            device_id,
            name=intf.get("name"),
            mac=intf.get("mac"),
            ip=intf.get("ip"),
            status=intf.get("status"),
            description=intf.get("description")
        )


# ------------------------------
# Funciones de compatibilidad antigua
# ------------------------------
def add_interface(device_id, name, mac=None, ip=None, status=None, description=None):
    add_or_update_interface(device_id, name, mac, ip, status, description)


def add_device(name, type_, ip, mac=None, model=None, location=None):
    return add_or_update_device(name, type_, ip, mac, model, location)


# ------------------------------
# Inicialización si se ejecuta directamente
# ------------------------------
if __name__ == "__main__":
    init_db()
