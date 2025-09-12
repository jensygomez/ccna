# modules/bastion_router/connect_bastion.py
from netmiko import ConnectHandler
import sqlite3
from modules.database_manager.db_utils import init_db, add_device, add_interface
import re

# Inicializar la base de datos
init_db()

# Datos de conexión al Bastion
BASTION = {
    "device_type": "cisco_ios",
    "host": "192.168.18.110",
    "username": "bastion",
    "password": "bastion",
    "secret": "bastion",
}

DB_PATH = "modules/database/net_devices.db"

def parse_interfaces(output):
    """
    Convierte el output de 'show ip interface brief' en una lista de dicts
    """
    interfaces = []
    lines = output.splitlines()
    for line in lines[1:]:
        if line.strip() == "":
            continue
        parts = re.split(r'\s+', line)
        if len(parts) < 6:
            continue
        iface = {
            "name": parts[0],
            "ip": parts[1],
            "status": parts[4],
            "protocol": parts[5],
            "description": ""  # Podrías extraer con 'show run' si quieres
        }
        interfaces.append(iface)
    return interfaces

def connect_to_bastion():
    try:
        net_connect = ConnectHandler(**BASTION)
        net_connect.enable()
        output = net_connect.send_command("show ip interface brief")
        interfaces = parse_interfaces(output)

        # Guardar/actualizar en la base de datos
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Agregar el dispositivo si no existe
        cursor.execute("SELECT id FROM devices WHERE ip=?", (BASTION["host"],))
        row = cursor.fetchone()
        if row:
            device_id = row[0]
        else:
            device_id = add_device(
                name="Bastion",
                type_="Router",
                ip=BASTION["host"],
                mac="N/A",
                model="ISR4331",
                location="Home Lab"
            )

        # Insertar o actualizar interfaces
        for iface in interfaces:
            cursor.execute("SELECT id, ip, status, description FROM interfaces WHERE device_id=? AND name=?",
                           (device_id, iface["name"]))
            existing = cursor.fetchone()
            if existing:
                # Actualizar solo si cambió algo
                iface_id, old_ip, old_status, old_desc = existing
                if old_ip != iface["ip"] or old_status != iface["status"] or old_desc != iface["description"]:
                    cursor.execute("""
                        UPDATE interfaces
                        SET ip=?, status=?, description=?, updated_at=CURRENT_TIMESTAMP
                        WHERE id=?
                    """, (iface["ip"], iface["status"], iface["description"], iface_id))
            else:
                # Insertar nueva interfaz
                add_interface(device_id, iface["name"], mac="N/A", ip=iface["ip"],
                              status=iface["status"], description=iface["description"])

        conn.commit()
        conn.close()
        net_connect.disconnect()
        return interfaces

    except Exception as e:
        print(f"⚠ Error connecting to Bastion: {e}")
        return None
