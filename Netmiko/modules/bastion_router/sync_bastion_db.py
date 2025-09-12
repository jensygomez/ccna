
# modules/bastion_router/sync_bastion_db.py
from .connect_bastion import connect_to_bastion
from modules.database_manager.db_utils import init_db, add_device, add_interface, update_interface_mac, add_log
import sqlite3
import re


DB_PATH = "modules/database/net_devices.db"

def parse_interfaces(output):
    """
    Recibe la salida de 'show ip interface brief' o 'show interface'
    y devuelve una lista de diccionarios con: name, ip, mac, status, protocol
    """
    interfaces = []
    lines = output.splitlines()
    for line in lines:
        # Evitamos líneas vacías o encabezados
        if re.match(r'^\s*(Interface|---)', line) or line.strip() == "":
            continue

        # Ejemplo: GigabitEthernet0/0         192.168.18.110  YES manual up                    up
        parts = line.split()
        if len(parts) >= 6:
            name = parts[0]
            ip = parts[1]
            status = parts[-2]
            protocol = parts[-1]
            # Inicializamos MAC como N/A, luego podemos intentar obtenerla con show interface
            interfaces.append({"name": name, "ip": ip, "mac": "N/A", "status": status, "protocol": protocol})
    return interfaces

def sync_interfaces():
    print("🔹 Connecting to Bastion to sync interfaces...")
    output = connect_to_bastion()
    if not output:
        print("❌ Could not retrieve interfaces from Bastion.")
        return

    interfaces = parse_interfaces(output)

    # Inicializamos DB
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verificamos que el dispositivo Bastion esté en la DB
    cursor.execute("SELECT id FROM devices WHERE ip=?", ("192.168.18.110",))
    row = cursor.fetchone()
    if row:
        device_id = row[0]
    else:
        device_id = add_device(
            name="Bastion",
            type_="Router",
            ip="192.168.18.110",
            mac="N/A",
            model="ISR4331",
            location="Home Lab"
        )

    # Iteramos interfaces y actualizamos DB
    for iface in interfaces:
        # Verificamos si la interfaz ya existe
        cursor.execute("SELECT id, mac FROM interfaces WHERE device_id=? AND name=?", (device_id, iface["name"]))
        row = cursor.fetchone()
        if row:
            iface_id, mac_db = row
            if mac_db != iface["mac"] and iface["mac"] != "N/A":
                update_interface_mac(iface_id, iface["mac"])
                add_log(device_id, f"Updated MAC for {iface['name']}", f"{mac_db} -> {iface['mac']}")
                print(f"⚡ Updated MAC for {iface['name']}: {mac_db} -> {iface['mac']}")
        else:
            add_interface(device_id, iface["name"], iface["mac"], iface["ip"], iface["status"])
            add_log(device_id, f"Added interface {iface['name']}", str(iface))
            print(f"➕ Added new interface {iface['name']}")

    conn.commit()
    conn.close()
    print("✅ Bastion interfaces synchronized with database.")

if __name__ == "__main__":
    sync_interfaces()
