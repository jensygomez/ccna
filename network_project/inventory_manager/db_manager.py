# network_project/inventory_manager/db_manager.py
import sqlite3

DB_FILE = "cisco_inventory.db"

def connect():
    return sqlite3.connect(DB_FILE)

# ---------------------------
# Dispositivos
# ---------------------------
def add_device(name, dev_type, ip=None, username=None, password=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO devices (name, type, ip_management, username, password)
        VALUES (?, ?, ?, ?, ?)
    """, (name, dev_type, ip, username, password))
    conn.commit()
    conn.close()

def list_devices():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, ip_management, username, password FROM devices")
    devices = cursor.fetchall()
    conn.close()
    return devices

def get_device(device_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, ip_management, username, password FROM devices WHERE id=?", (device_id,))
    device = cursor.fetchone()
    conn.close()
    return device

def update_device(device_id, **kwargs):
    conn = connect()
    cursor = conn.cursor()
    fields = []
    values = []
    for key, value in kwargs.items():
        fields.append(f"{key}=?")
        values.append(value)
    values.append(device_id)
    cursor.execute(f"UPDATE devices SET {', '.join(fields)} WHERE id=?", values)
    conn.commit()
    conn.close()

def delete_device(device_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM devices WHERE id=?", (device_id,))
    conn.commit()
    conn.close()

# ---------------------------
# Interfaces
# ---------------------------
def add_interface(device_id, name, ip=None, status=None, mode=None, description=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO interfaces (device_id, name, ip, status, mode, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (device_id, name, ip, status, mode, description))
    conn.commit()
    conn.close()

def list_interfaces(device_id=None):
    conn = connect()
    cursor = conn.cursor()
    if device_id:
        cursor.execute("SELECT * FROM interfaces WHERE device_id=?", (device_id,))
    else:
        cursor.execute("SELECT * FROM interfaces")
    interfaces = cursor.fetchall()
    conn.close()
    return interfaces

# ---------------------------
# VLANs
# ---------------------------
def add_vlan(name, number, description=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vlans (name, number, description) VALUES (?, ?, ?)", (name, number, description))
    conn.commit()
    conn.close()

def list_vlans():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vlans")
    vlans = cursor.fetchall()
    conn.close()
    return vlans

# ---------------------------
# Relación dispositivos - VLANs
# ---------------------------
def assign_vlan_to_device(device_id, vlan_id, interfaces=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO device_vlans (device_id, vlan_id, interfaces) VALUES (?, ?, ?)
    """, (device_id, vlan_id, interfaces))
    conn.commit()
    conn.close()
