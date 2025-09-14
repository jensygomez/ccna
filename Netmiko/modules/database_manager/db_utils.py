#Netmiko/modules/database_manager/db_utils.py
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
        ip TEXT UNIQUE,
        mac TEXT UNIQUE,
        model TEXT,
        location TEXT,
        registered_at TIMESTAMP
    )
    """)
    
    # Crear tabla credentials
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER UNIQUE,
        username TEXT,
        password TEXT,
        secret TEXT,
        FOREIGN KEY (device_id) REFERENCES devices (id) ON DELETE CASCADE
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
        last_seen TIMESTAMP,
        FOREIGN KEY (device_id) REFERENCES devices (id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    conn.close()

# --------- Bastion ---------
def get_bastion_credentials():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.ip, c.username, c.password, c.secret, d.id
        FROM devices d
        JOIN credentials c ON c.device_id = d.id
        WHERE d.name='Bastion'
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"host": row[0], "username": row[1], "password": row[2], "secret": row[3], "device_id": row[4]}
    return None

def add_or_update_bastion(host, username, password, secret, name="Bastion"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Verificar si ya existe
        cursor.execute("SELECT id FROM devices WHERE name=?", (name,))
        row = cursor.fetchone()
        
        if row:
            device_id = row[0]
            # Actualizar
            cursor.execute("UPDATE devices SET ip=?, registered_at=? WHERE id=?", 
                           (host, datetime.now(), device_id))
            cursor.execute("UPDATE credentials SET username=?, password=?, secret=? WHERE device_id=?",
                           (username, password, secret, device_id))
        else:
            cursor.execute("INSERT INTO devices (name, ip, registered_at) VALUES (?, ?, ?)",
                           (name, host, datetime.now()))
            device_id = cursor.lastrowid
            cursor.execute("INSERT INTO credentials (device_id, username, password, secret) VALUES (?, ?, ?, ?)",
                           (device_id, username, password, secret))
        
        conn.commit()
        return device_id
        
    except sqlite3.IntegrityError as e:
        print(f"❌ Error de integridad: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

# --------- Devices ---------
def find_device_by_identifiers(name=None, ip=None, mac=None):
    """
    Busca un dispositivo usando múltiples identificadores
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    device_id = None
    
    # 1. Buscar por IP (más confiable)
    if ip:
        cursor.execute("SELECT id FROM devices WHERE ip=?", (ip,))
        row = cursor.fetchone()
        if row:
            device_id = row[0]
            print(f"    ✅ Encontrado por IP: {ip} -> ID: {device_id}")
    
    # 2. Buscar por MAC (muy confiable)
    if not device_id and mac:
        cursor.execute("SELECT id FROM devices WHERE mac=?", (mac,))
        row = cursor.fetchone()
        if row:
            device_id = row[0]
            print(f"    ✅ Encontrado por MAC: {mac} -> ID: {device_id}")
    
    # 3. Buscar por nombre (solo si no es genérico)
    if not device_id and name and name != "N/A" and not name.startswith(("Device-", "Unknown-")):
        cursor.execute("SELECT id FROM devices WHERE name=?", (name,))
        row = cursor.fetchone()
        if row:
            device_id = row[0]
            print(f"    ✅ Encontrado por nombre: {name} -> ID: {device_id}")
    
    conn.close()
    return device_id

def add_or_update_device(name, type_, ip=None, mac=None, model=None, location=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Buscar dispositivo existente
        device_id = find_device_by_identifiers(name, ip, mac)
        
        if device_id:
            # Actualizar dispositivo existente
            update_fields = []
            update_values = []
            
            if name and name != "N/A": 
                update_fields.append("name=?")
                update_values.append(name)
            if type_: 
                update_fields.append("type=?")
                update_values.append(type_)
            if ip: 
                update_fields.append("ip=?")
                update_values.append(ip)
            if mac: 
                update_fields.append("mac=?")
                update_values.append(mac)
            if model: 
                update_fields.append("model=?")
                update_values.append(model)
            if location: 
                update_fields.append("location=?")
                update_values.append(location)
            
            update_fields.append("registered_at=?")
            update_values.append(datetime.now())
            update_values.append(device_id)
            
            if update_fields:
                cursor.execute(f"UPDATE devices SET {', '.join(update_fields)} WHERE id=?", update_values)
        else:
            # Insertar nuevo dispositivo
            cursor.execute("""
                INSERT INTO devices (name, type, ip, mac, model, location, registered_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, type_, ip, mac, model, location, datetime.now()))
            device_id = cursor.lastrowid
        
        conn.commit()
        return device_id
        
    except sqlite3.IntegrityError as e:
        print(f"❌ Error de integridad: {e}")
        # Intentar recuperar el ID existente
        if ip:
            cursor.execute("SELECT id FROM devices WHERE ip=?", (ip,))
            row = cursor.fetchone()
            if row:
                return row[0]
        conn.rollback()
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_devices():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows

# --------- LLDP Neighbors ---------
def add_or_update_lldp_neighbor(device_id, local_interface, neighbor_name, neighbor_port,
                                neighbor_ip=None, neighbor_type=None, neighbor_model=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Primero verificar si ya existe
        cursor.execute("""
            SELECT id FROM lldp_neighbors 
            WHERE device_id=? AND local_interface=? AND neighbor_name=?
        """, (device_id, local_interface, neighbor_name))
        
        row = cursor.fetchone()
        
        if row:
            # Actualizar existente
            cursor.execute("""
                UPDATE lldp_neighbors 
                SET neighbor_port=?, neighbor_ip=?, neighbor_type=?, neighbor_model=?, last_seen=?
                WHERE id=?
            """, (neighbor_port, neighbor_ip, neighbor_type, neighbor_model, datetime.now(), row[0]))
        else:
            # Insertar nuevo
            cursor.execute("""
                INSERT INTO lldp_neighbors 
                (device_id, local_interface, neighbor_name, neighbor_port, neighbor_ip, neighbor_type, neighbor_model, last_seen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (device_id, local_interface, neighbor_name, neighbor_port,
                  neighbor_ip, neighbor_type, neighbor_model, datetime.now()))

        conn.commit()
        
    except Exception as e:
        print(f"❌ Error al agregar vecino LLDP: {e}")
        conn.rollback()
    finally:
        conn.close()