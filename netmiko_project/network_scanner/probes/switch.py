# netmiko_project/network_scanner/probes/switch.py
"""
Funciones específicas para switches.
"""

def get_interfaces(conn):
    """Obtiene interfaces y estado."""
    output = conn.send_command("show ip interface brief", use_textfsm=True)
    return output

def get_mac_table(conn):
    """Obtiene tabla MAC."""
    output = conn.send_command("show mac address-table", use_textfsm=True)
    return output

def get_lldp_neighbors(conn):
    """Obtiene vecinos LLDP"""
    neighbors_raw = conn.send_command("show lldp neighbors detail", use_textfsm=True)
    # Añadimos IP y name si existe
    neighbors = []
    for n in neighbors_raw:
        neighbors.append({
            "neighbor": n.get("neighbor") or "",
            "port": n.get("port") or "",
            "neighbor_ip": n.get("management_ip") or None,
            "credentials": n.get("credentials") or None  # opcional, para cascada
        })
    return neighbors