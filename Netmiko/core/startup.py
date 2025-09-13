#Netmiko/core/startup.py
from .scanner import scan_network
from .sync import sync_devices_to_db
import sqlite3

DB_PATH = "modules/database/net_devices.db"

def startup():
    print("🔹 Iniciando Network Manager...\n")

    # 🔍 Escaneo simple de la red
    network_cidr = "192.168.0.0/24"
    print(f"📊 Escaneando red {network_cidr}...")
    active_ips = scan_network(network_cidr)

    # Simulación de identificación de dispositivos
    devices = []
    for ip in active_ips:
        if ip.endswith(".1"):
            devices.append({"ip": ip, "name": "Bastion", "type": "Router"})
        elif ip.endswith(".111"):
            devices.append({"ip": ip, "name": "Sw-Core-111", "type": "Switch"})
        else:
            devices.append({"ip": ip, "name": f"Host-{ip}", "type": "Unknown"})

    # 🔄 Sincronizar con DB
    print("\n🔄 Sincronizando con base de datos...")
    sync_devices_to_db(devices)

    # 📊 Mostrar inventario
    print("\n=== Network Inventory ===")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, ip FROM devices")
    rows = cursor.fetchall()
    conn.close()

    print("+----+-------------+----------+----------------+")
    print("| ID |    Nombre   |   Tipo   |       IP       |")
    print("+----+-------------+----------+----------------+")
    for row in rows:
        print(f"| {row[0]:<2} | {row[1]:<11} | {row[2]:<8} | {row[3]:<14} |")
    print("+----+-------------+----------+----------------+")
