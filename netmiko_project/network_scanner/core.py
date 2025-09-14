# netmiko_project/network_scanner/core.py
"""
network_scanner/core.py
Scanner de inventario real: detecta hosts activos, se conecta vía SSH,
obtiene interfaces, tabla MAC, ARP y vecinos LLDP.
"""

import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException
from probes import switch, router

DEFAULT_WORKERS = 20
RESULTS_FILE = "inventory_results.json"
SSH_PORT = 22
SSH_TIMEOUT = 5

def ping_host(ip):
    """Ping simple para ver si host está activo (ICMP)."""
    import subprocess, platform
    param = "-n" if platform.system().lower()=="windows" else "-c"
    try:
        res = subprocess.run(["ping", param, "1", "-W", "1", ip],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception:
        return False

def test_ssh(ip, username, password):
    """Prueba conexión SSH al host."""
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
        "port": SSH_PORT,
        "timeout": SSH_TIMEOUT,
    }
    try:
        with ConnectHandler(**device) as conn:
            return conn
    except (NetMikoAuthenticationException, NetMikoTimeoutException):
        return None

def scan_host(ip, creds):
    """Escaneo completo de un host."""
    result = {"ip": ip, "active": False, "interfaces": None, "mac_table": None, "arp_table": None, "lldp": None}
    if not ping_host(ip):
        return result
    result["active"] = True

    for user, pwd in creds:
        conn = test_ssh(ip, user, pwd)
        if conn:
            # Determinar tipo de dispositivo (switch/router) según heurística simple
            try:
                prompt = conn.find_prompt()
                if any(x in prompt.lower() for x in ["switch"]):
                    result["interfaces"] = switch.get_interfaces(conn)
                    result["mac_table"] = switch.get_mac_table(conn)
                    result["lldp"] = switch.get_lldp_neighbors(conn)
                else:
                    result["interfaces"] = router.get_interfaces(conn)
                    result["arp_table"] = router.get_arp_table(conn)
            finally:
                conn.disconnect()
            break  # no probar más credenciales si conectó
    return result

def run_inventory_from_config(config_path, workers=None):
    """Carga config JSON y ejecuta el inventario completo."""
    config_path = Path(config_path)
    if not config_path.exists():
        print(f"[ERROR] No existe config: {config_path}")
        return False

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    targets = cfg.get("targets", [])
    creds = cfg.get("credentials", [])  # [{"user":"cisco","password":"cisco"}]
    workers = workers or cfg.get("workers", DEFAULT_WORKERS)

    results = []
    print(f"[scanner] Hosts a escanear: {len(targets)}, workers={workers}")

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(scan_host, ip, creds): ip for ip in targets}
        for future in as_completed(futures):
            try:
                r = future.result()
                results.append(r)
                print(f"[scanner] {r['ip']} -> active={r['active']}")
            except Exception as e:
                print(f"[scanner] error host {futures[future]}: {e}")

    out_file = Path(cfg.get("output", RESULTS_FILE))
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"scanned_at": time.strftime("%Y-%m-%d %H:%M:%S"), "results": results}, f, indent=2)

    print(f"[scanner] Inventario guardado en {out_file}")
    return True
