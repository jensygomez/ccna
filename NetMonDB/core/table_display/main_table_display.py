# NetMonDB/core/table_display/main_table_display.py

import os
import json
from tabulate import tabulate

OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "../../outputs")

def table_main():
    """
    Muestra todos los dispositivos registrados en outputs/*.json
    mostrando interfaces con IP y también interfaces activas sin IP.
    """
    devices = []
    
    # Leer todos los JSON en la carpeta outputs
    for filename in os.listdir(OUTPUTS_DIR):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(OUTPUTS_DIR, filename)
        with open(path, "r") as f:
            data = json.load(f)

        hostname = data.get("hostname", "N/A")

        # Extraer interfaces con IP y activas sin IP
        interfaces_ip = []
        interfaces_up = []
        running_config = data.get("show_running_config", "")
        current_iface = None
        for line in running_config.splitlines():
            line = line.strip()
            if line.lower().startswith("interface "):
                current_iface = line.split()[1]
                ip_found = False
            elif current_iface:
                if line.lower().startswith("ip address") and "0.0.0.0" not in line:
                    ip = line.split()[2]
                    mask = line.split()[3]
                    interfaces_ip.append(f"{current_iface} {ip}/{mask}")
                    ip_found = True
                elif line.lower().startswith("shutdown"):
                    # Si está shutdown, no la marcamos
                    pass
                elif line and not ip_found:
                    # Si hay configuración pero sin IP ni shutdown, la marcamos como activa
                    interfaces_up.append(current_iface)

        # Eliminar duplicados en interfaces_up
        interfaces_up = [i for i in interfaces_up if i not in [x.split()[0] for x in interfaces_ip]]

        # Extraer rutas estáticas
        static_routes = []
        for line in running_config.splitlines():
            line = line.strip()
            if line.lower().startswith("ip route") and "0.0.0.0 0.0.0.0" not in line:
                static_routes.append(line)

        # Vecinos LLDP/CDP
        neighbors = []
        if "lldp run" in running_config.lower():
            neighbors.append("LLDP activo")
        if "cdp run" in running_config.lower():
            neighbors.append("CDP activo")
        if not neighbors:
            neighbors = ["N/A"]

        devices.append({
            "hostname": hostname,
            "interfaces_ip": interfaces_ip if interfaces_ip else ["N/A"],
            "interfaces_up": interfaces_up if interfaces_up else [],
            "static_routes": static_routes if static_routes else ["N/A"],
            "neighbors": ", ".join(neighbors)
        })

    # Preparar tabla
    rows = []
    for dev in devices:
        interfaces_display = []
        if dev["interfaces_ip"] != ["N/A"]:
            interfaces_display.extend(dev["interfaces_ip"])
        if dev["interfaces_up"]:
            interfaces_display.extend([f"{i} (UP sin IP)" for i in dev["interfaces_up"]])
        if not interfaces_display:
            interfaces_display = ["N/A"]

        rows.append([
            dev["hostname"],
            "\n".join(interfaces_display),
            "\n".join(dev["static_routes"]),
            dev["neighbors"]
        ])

    headers = ["Hostname", "Interfaces con IP / Activas", "Rutas estáticas", "Vecinos LLDP/CDP"]

    if rows:
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
    else:
        print("⚠️ No hay datos de dispositivos para mostrar.")
