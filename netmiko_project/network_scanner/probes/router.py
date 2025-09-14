# netmiko_project/network_scanner/probes/router.py
"""
Funciones específicas para routers.
"""

def get_interfaces(conn):
    """Obtiene interfaces y estado"""
    output = conn.send_command("show ip interface brief", use_textfsm=True)
    return output

def get_arp_table(conn):
    """Obtiene tabla ARP"""
    output = conn.send_command("show arp", use_textfsm=True)
    return output
