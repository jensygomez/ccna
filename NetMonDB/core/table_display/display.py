# NetMonDB/core/table_display/display.py

# core/table_display/display.py
from tabulate import tabulate

def show_table(parsed_data):
    if not parsed_data:
        print("⚠️ No hay datos para mostrar en tabla.")
        return

    hostname = parsed_data.get("hostname", "N/A")

    # Interfaces con IP
    interfaces = parsed_data.get("interfaces", {})
    interfaces_with_ip = []
    for intf, details in interfaces.items():
        ip = details.get("ip_address")
        if ip:
            interfaces_with_ip.append(f"{intf}: {ip}")
    interfaces_str = "\n".join(interfaces_with_ip) if interfaces_with_ip else "N/A"

    # Rutas estáticas
    routes = parsed_data.get("ip_routes", [])
    routes_str = "\n".join([f"{r['dest']} → {r['gateway']}" for r in routes]) if routes else "N/A"

    # Vecinos LLDP/CDP
    neighbors = parsed_data.get("neighbors", [])
    neighbors_str = "\n".join([f"{n['neighbor']} ({n['port']})" for n in neighbors]) if neighbors else "N/A"

    # Crear lista de filas
    table = [[hostname, interfaces_str, routes_str, neighbors_str]]

    # Encabezados
    headers = ["Hostname", "Interfaces con IP", "Rutas estáticas", "Vecinos LLDP/CDP"]

    # Imprimir con tabulate
    print(tabulate(table, headers=headers, tablefmt="grid", stralign="left"))


