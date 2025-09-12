
# modules/bastion_router/connect_bastion.py
from netmiko import ConnectHandler
import re

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
