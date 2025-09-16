# NetMonDB/core/table_display/display.py

# core/table_display/display.py
import os
import json
from tabulate import tabulate

OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "../../outputs")

def table_main():
    """Muestra todos los dispositivos con sus interfaces, rutas y vecinos."""
    if not os.path.exists(OUTPUTS_DIR):
        print(f"⚠️ Carpeta de outputs no encontrada: {OUTPUTS_DIR}")
        return

    table = []
    # Recorremos todos los archivos JSON en outputs/
    for filename in os.listdir(OUTPUTS_DIR):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(OUTPUTS_DIR, filename)
        with open(filepath, "r") as f:
            data = json.load(f)

        hostname = data.get("hostname", "N/A")
        interfaces_str = "\n".join(data.get("interfaces", ["N/A"]))
        routes_str = "\n".join(data.get("static_routes", ["N/A"]))
        neighbors_str = "\n".join(data.get("neighbors", ["N/A"]))

        table.append([hostname, interfaces_str, routes_str, neighbors_str])

    if not table:
        print("⚠️ No hay datos para mostrar.")
        return

    headers = ["Hostname", "Interfaces con IP / Activas", "Rutas estáticas", "Vecinos LLDP/CDP"]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid", stralign="left"))
