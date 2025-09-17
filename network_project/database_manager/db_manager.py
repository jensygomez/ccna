# network_project/inventory_manager/db_manager.py


import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "database_manager", "cisco_inventory.db")
DB_FILE = os.path.abspath(DB_FILE)

def connect():
    return sqlite3.connect(DB_FILE)

def update_record(table, record_id, **fields):
    """
    Actualiza cualquier registro de cualquier tabla.
    `fields` es un diccionario {columna: valor}.
    """
    if not fields:
        return
    conn = connect()
    cursor = conn.cursor()
    set_clause = ", ".join(f"{k}=?" for k in fields.keys())
    values = list(fields.values()) + [record_id]
    cursor.execute(f"UPDATE {table} SET {set_clause} WHERE id=?", values)
    conn.commit()
    conn.close()

def delete_record(table, record_id):
    """
    Elimina cualquier registro de cualquier tabla por ID.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE id=?", (record_id,))
    conn.commit()
    conn.close()



# ---------------------------
# DISPOSITIVOS
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

def list_devices(full=False):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, ip_management, username, password FROM devices")
    devices = cursor.fetchall()
    conn.close()

    if full:
        result = []
        for d in devices:
            dev_id = d[0]
            interfaces = list_interfaces(dev_id)
            vlans = list_device_vlans(dev_id)
            extra = list_extra_attributes(dev_id)
            result.append({
                "id": dev_id,
                "name": d[1],
                "type": d[2],
                "ip_management": d[3],
                "username": d[4],
                "password": d[5],
                "interfaces": interfaces,
                "vlans": vlans,
                "extra": extra
            })
        return result
    else:
        return devices

def get_device(device_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, ip_management, username, password FROM devices WHERE id=?", (device_id,))
    device = cursor.fetchone()
    conn.close()
    return device

def update_device(device_id, **kwargs):
    if not kwargs:
        return
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
# INTERFACES
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
        cursor.execute("SELECT id, name, ip, status, mode, description FROM interfaces WHERE device_id=?", (device_id,))
    else:
        cursor.execute("SELECT id, device_id, name, ip, status, mode, description FROM interfaces")
    interfaces = cursor.fetchall()
    conn.close()
    return interfaces

def update_interface(interface_id, **kwargs):
    if not kwargs:
        return
    conn = connect()
    cursor = conn.cursor()
    fields = [f"{k}=?" for k in kwargs.keys()]
    values = list(kwargs.values())
    values.append(interface_id)
    cursor.execute(f"UPDATE interfaces SET {', '.join(fields)} WHERE id=?", values)
    conn.commit()
    conn.close()

def delete_interface(interface_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM interfaces WHERE id=?", (interface_id,))
    conn.commit()
    conn.close()


def list_all_interfaces():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id, d.name, i.name, i.ip, i.status, i.mode, i.description
        FROM interfaces i
        JOIN devices d ON i.device_id = d.id
    """)
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
    cursor.execute("SELECT id, name, number, description FROM vlans")
    vlans = cursor.fetchall()
    conn.close()
    return vlans

def update_vlan(vlan_id, **kwargs):
    if not kwargs:
        return
    conn = connect()
    cursor = conn.cursor()
    fields = [f"{k}=?" for k in kwargs.keys()]
    values = list(kwargs.values())
    values.append(vlan_id)
    cursor.execute(f"UPDATE vlans SET {', '.join(fields)} WHERE id=?", values)
    conn.commit()
    conn.close()

def delete_vlan(vlan_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vlans WHERE id=?", (vlan_id,))
    conn.commit()
    conn.close()

# ---------------------------
# DEVICE-VLAN (asignación)
# ---------------------------
def assign_vlan_to_device(device_id, vlan_id, interfaces=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO device_vlans (device_id, vlan_id, interfaces)
        VALUES (?, ?, ?)
    """, (device_id, vlan_id, interfaces))
    conn.commit()
    conn.close()

def list_device_vlans(device_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dv.id, v.name, v.number, dv.interfaces
        FROM device_vlans dv
        JOIN vlans v ON dv.vlan_id = v.id
        WHERE dv.device_id=?
    """, (device_id,))
    vlans = cursor.fetchall()
    conn.close()
    return vlans

# ---------------------------
# PROTOCOLS
# ---------------------------
def add_protocol(name, description=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO protocols (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    conn.close()

def list_protocols():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM protocols")
    protocols = cursor.fetchall()
    conn.close()
    return protocols

def assign_protocol_to_device(device_id, protocol_id, config=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO device_protocols (device_id, protocol_id, config)
        VALUES (?, ?, ?)
    """, (device_id, protocol_id, config))
    conn.commit()
    conn.close()

def list_device_protocols(device_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dp.id, p.name, dp.config
        FROM device_protocols dp
        JOIN protocols p ON dp.protocol_id = p.id
        WHERE dp.device_id=?
    """, (device_id,))
    result = cursor.fetchall()
    conn.close()
    return result

# ---------------------------
# ROUTES
# ---------------------------
def add_route(device_id, destination, mask, next_hop, protocol=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO routes (device_id, destination, mask, next_hop, protocol)
        VALUES (?, ?, ?, ?, ?)
    """, (device_id, destination, mask, next_hop, protocol))
    conn.commit()
    conn.close()

def list_routes(device_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, destination, mask, next_hop, protocol FROM routes WHERE device_id=?", (device_id,))
    routes = cursor.fetchall()
    conn.close()
    return routes

def delete_route(route_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM routes WHERE id=?", (route_id,))
    conn.commit()
    conn.close()

# ---------------------------
# LINKS (enlaces físicos)
# ---------------------------
def add_link(interface_a_id, interface_b_id, description=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO links (interface_a_id, interface_b_id, description)
        VALUES (?, ?, ?)
    """, (interface_a_id, interface_b_id, description))
    conn.commit()
    conn.close()

def list_links():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, interface_a_id, interface_b_id, description FROM links")
    links = cursor.fetchall()
    conn.close()
    return links

def delete_link(link_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM links WHERE id=?", (link_id,))
    conn.commit()
    conn.close()

# ---------------------------
# EXTRA ATTRIBUTES
# ---------------------------
def add_extra_attribute(device_id, name, value):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO extra_attributes (device_id, attribute_name, attribute_value)
        VALUES (?, ?, ?)
    """, (device_id, name, value))
    conn.commit()
    conn.close()

def list_extra_attributes(device_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, attribute_name, attribute_value FROM extra_attributes
        WHERE device_id=?
    """, (device_id,))
    attrs = cursor.fetchall()
    conn.close()
    return attrs


def update_extra_attribute(attr_id, value):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE extra_attributes SET attribute_value=? WHERE id=?", (value, attr_id))
    conn.commit()
    conn.close()

def delete_extra_attribute(attr_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM extra_attributes WHERE id=?", (attr_id,))
    conn.commit()
    conn.close()
