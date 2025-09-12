# modules/bastion_router/connect_bastion.py
from netmiko import ConnectHandler
import sqlite3
from modules.database_manager.db_utils import init_db, add_device, add_interface, update_interface_mac, add_log
import re

DB_PATH = "modules/database/net_devices.db"  # ruta relativa al proyecto

def connect_to_bastion():
    # Configuración SSH del Bastion
    bastion = {
        "device_type": "cisco_ios",
        "host": "192.168.18.110",
        "username": "bastion",
        "password": "bastion",
        "secret": "bastion",
    }

    try:
        conn = ConnectHandler(**bastion)
        conn.enable()
        
        # Obtenemos interfaces y estado
        output_brief = conn.send_command("show ip interface brief")
        output_int = conn.send_command("show interface")

        # Inicializamos DB
        init_db()

        # Agregamos el dispositivo si no existe
        device_id = add_device(
            name="Bastion",
            type_="Router",
            ip="192.168.18.110",
            mac="N/A",
            model="ISR4331",
            location="Home Lab"
        )

        # Conexión a DB
        conn_db = sqlite3.connect(DB_PATH)
        cursor = conn_db.cursor()

        # Parseamos interfaces
        interfaces = []
        lines = output_brief.splitlines()[1:]  # saltamos encabezado
        for line in lines:
            parts = line.split()
            if len(parts) >= 6:
                name, ip_addr, ok, method, status, proto = parts[:6]
                
                # Buscamos MAC real en "show interface"
                mac_match = re.search(
                    rf"{name}.*address is (\S+)", output_int, re.DOTALL
                )
                mac = mac_match.group(1) if mac_match else "N/A"

                # Revisamos si ya existe la interfaz
                cursor.execute("SELECT id, mac FROM interfaces WHERE device_id=? AND name=?", (device_id, name))
                row = cursor.fetchone()
                
                if row:
                    intf_id, old_mac = row
                    if mac != old_mac:
                        update_interface_mac(intf_id, mac)
                        add_log(device_id, f"MAC changed on {name}", f"{old_mac} -> {mac}")
                else:
                    # Si no existe, la agregamos
                    add_interface(
                        device_id=device_id,
                        name=name,
                        mac=mac,
                        ip=ip_addr,
                        status=status,
                        description=""
                    )

                interfaces.append({
                    "name": name,
                    "ip": ip_addr,
                    "mac": mac,
                    "status": status
                })

        conn_db.close()
        conn.disconnect()
        return interfaces

    except Exception as e:
        print(f"❌ Error connecting to Bastion: {e}")
        return None
