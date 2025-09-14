# netmiko_project/network_scanner/core.py
"""
network_scanner/core.py
Scanner en cascada: conecta al bastion y luego a cada switch/router descubierto,
obteniendo interfaces, MAC table y LLDP neighbors.
"""

import json
import time
from pathlib import Path
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException
from probes import switch, router

SCANNED_DEVICES = set()  # Para no escanear dos veces
RESULTS = []

def connect_device(ip, username, password):
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
        "timeout": 8
    }
    try:
        conn = ConnectHandler(**device)
        return conn
    except (NetMikoAuthenticationException, NetMikoTimeoutException) as e:
        print(f"[ERROR] No se pudo conectar a {ip}: {e}")
        return None

def scan_device(ip, username, password, device_name=None):
    """Escanea un dispositivo y sus vecinos recursivamente."""
    key = f"{ip}-{device_name or ip}"
    if key in SCANNED_DEVICES:
        return
    SCANNED_DEVICES.add(key)

    print(f"[SCAN] Conectando a {ip} ({device_name})...")
    conn = connect_device(ip, username, password)
    if not conn:
        RESULTS.append({"ip": ip, "device": device_name, "status": "failed"})
        return

    # Detectar tipo simple por nombre del prompt
    prompt = conn.find_prompt().lower()
    if "switch" in prompt:
        dev_type = "switch"
        interfaces = switch.get_interfaces(conn)
        mac_table = switch.get_mac_table(conn)
        lldp_neighbors = switch.get_lldp_neighbors(conn)
        device_info = {
            "ip": ip,
            "device": device_name,
            "type": dev_type,
            "interfaces": interfaces,
            "mac_table": mac_table,
            "lldp_neighbors": lldp_neighbors
        }
        RESULTS.append(device_info)

        # Escaneo en cascada de vecinos LLDP
        for neighbor in lldp_neighbors:
            n_ip = neighbor.get("management_ip") or neighbor.get("neighbor_ip")
            n_name = neighbor.get("neighbor")
            n_creds = neighbor.get("credentials")  # opcional: puedes pasar dict de credenciales
            if n_ip and n_creds:
                scan_device(n_ip, n_creds["user"], n_creds["password"], n_name)

    else:
        dev_type = "router"
        interfaces = router.get_interfaces(conn)
        arp_table = router.get_arp_table(conn)
        device_info = {
            "ip": ip,
            "device": device_name,
            "type": dev_type,
            "interfaces": interfaces,
            "arp_table": arp_table
        }
        RESULTS.append(device_info)

    conn.disconnect()

def run_inventory(devices, output_file="inventory_results.json"):
    """
    devices: lista de dicts con keys: ip, user, password, name (opcional)
    """
    for dev in devices:
        scan_device(dev["ip"], dev["user"], dev["password"], dev.get("name"))

    out_path = Path(output_file)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"scanned_at": time.strftime("%Y-%m-%d %H:%M:%S"), "results": RESULTS}, f, indent=2)

    print(f"[SCAN] Inventario guardado en {out_path}")
