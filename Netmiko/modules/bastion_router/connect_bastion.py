# modules/bastion_router/connect_bastion.py
from netmiko import ConnectHandler
import re
from datetime import datetime

def get_lldp_neighbors(conn):
    """
    Devuelve una lista de vecinos LLDP con información detallada:
    local_intf, neighbor_name, neighbor_port, neighbor_ip, neighbor_type, neighbor_model, timestamp
    """
    output = conn.send_command("show lldp neighbors detail")
    neighbors = []

    blocks = output.split("\n\n")  # separar cada vecino
    for block in blocks:
        neighbor = {}
        # Device ID
        match_name = re.search(r"Device ID: (\S+)", block)
        if match_name:
            neighbor["neighbor_name"] = match_name.group(1)
        else:
            continue

        # Puerto local
        match_local = re.search(r"Local Intf: (\S+ \S+)", block)
        neighbor["local_intf"] = match_local.group(1) if match_local else "N/A"

        # Puerto remoto
        match_remote = re.search(r"Port id: (\S+)", block)
        neighbor["neighbor_port"] = match_remote.group(1) if match_remote else "N/A"

        # Tipo / capacidades
        match_type = re.search(r"System Capabilities: (.+)", block)
        neighbor["neighbor_type"] = match_type.group(1) if match_type else "N/A"

        # Modelo / descripción
        match_model = re.search(r"System Description: (.+)", block, re.DOTALL)
        neighbor["neighbor_model"] = match_model.group(1).strip() if match_model else "N/A"

        # IP de gestión
        match_ip = re.search(r"Management Address: (\S+)", block)
        neighbor["neighbor_ip"] = match_ip.group(1) if match_ip else None

        # Timestamp
        neighbor["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        neighbors.append(neighbor)

    return neighbors


def connect_to_bastion():
    """
    Conecta al Bastion y devuelve una lista de interfaces con:
    name, ip, mac, status
    """
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
        print("✅ Conectado al Bastion")

        # Obtenemos salidas
        output_brief = conn.send_command("show ip interface brief")
        output_int = conn.send_command("show interface")

        interfaces = []
        lines = output_brief.splitlines()[1:]  # saltamos encabezado
        for line in lines:
            parts = line.split()
            if len(parts) >= 6:
                name, ip_addr, _, _, status, proto = parts[:6]

                # Buscamos la MAC real en "show interface"
                mac_match = re.search(
                    rf"{name}.*address is (\S+)", output_int, re.DOTALL
                )
                mac = mac_match.group(1) if mac_match else "N/A"

                interfaces.append({
                    "name": name,
                    "ip": ip_addr if ip_addr != "unassigned" else None,
                    "mac": mac,
                    "status": f"{status}/{proto}"
                })

        conn.disconnect()
        return interfaces

    except Exception as e:
        print(f"❌ Error al conectar al Bastion: {e}")
        return None
