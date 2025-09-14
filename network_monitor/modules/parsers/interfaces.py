# network_monitor/modules/parsers/interfaces.py
import re

def parse_interfaces(output):
    """
    Extrae de 'show ip interface brief' la info:
    Interface, IP-Address, OK?, Method, Status, Protocol
    Retorna lista de dicts.
    """
    interfaces = []
    lines = output.splitlines()
    for line in lines[1:]:  # Saltamos header
        if line.strip() == "":
            continue
        parts = re.split(r'\s+', line)
        if len(parts) >= 6:
            interfaces.append({
                "name": parts[0],
                "ip": parts[1],
                "status": parts[4],
                "protocol": parts[5]
            })
    return interfaces
