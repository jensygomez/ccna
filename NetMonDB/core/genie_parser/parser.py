# NetMonDB/core/genie_parser/parser.py

# NetMonDB/core/genie_parser/parser.py
import re

def parse_show_with_genie(raw_output):
    """
    Extrae datos mínimos del running-config:
    - Hostname
    - Interfaces con IP
    - Rutas estáticas
    - Vecinos LLDP/CDP (solo menciona si lldp run está activo)
    """
    result = {}

    # 1️⃣ Hostname
    match = re.search(r"^hostname (\S+)", raw_output, re.MULTILINE)
    result['hostname'] = match.group(1) if match else "N/A"

    # 2️⃣ Interfaces con IP
    interfaces = []
    iface_blocks = re.findall(r"interface (\S+)(.*?)(?=^interface|\Z)", raw_output, re.MULTILINE | re.DOTALL)
    for iface, config in iface_blocks:
        ip_match = re.search(r"ip address (\S+) (\S+)", config)
        if ip_match:
            interfaces.append(f"{iface}: {ip_match.group(1)}/{ip_match.group(2)}")
    result['interfaces'] = interfaces if interfaces else ["N/A"]

    # 3️⃣ Rutas estáticas
    routes = re.findall(r"ip route (\S+) (\S+) (\S+)", raw_output)
    result['static_routes'] = [f"{dst} {mask} {gw}" for dst, mask, gw in routes] if routes else ["N/A"]

    # 4️⃣ Vecinos LLDP/CDP
    result['neighbors'] = []
    if re.search(r"^lldp run", raw_output, re.MULTILINE):
        result['neighbors'].append("LLDP")
    if re.search(r"^cdp run", raw_output, re.MULTILINE):
        result['neighbors'].append("CDP")
    if not result['neighbors']:
        result['neighbors'] = ["N/A"]

    # 5️⃣ Guardar en JSON
    import json, os
    os.makedirs("outputs", exist_ok=True)
    filename = f"outputs/{result['hostname']}_running_config.json"
    with open(filename, "w") as f:
        json.dump(result, f, indent=4)

    return result
