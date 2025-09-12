# modules/database_manager/db_viewer.py
import sqlite3
import os
from tabulate import tabulate

# Ruta a la base de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "net_devices.db")


def view_devices():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, ip, mac, model, location, registered_at FROM devices")
    rows = cursor.fetchall()
    conn.close()

    print("\n=== DEVICES ===")
    print(tabulate(rows, headers=["ID", "Name", "Type", "IP", "MAC", "Model", "Location", "Registered"], tablefmt="pretty"))


def view_interfaces(device_id=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if device_id:
        cursor.execute("SELECT id, device_id, name, mac, ip, status, description, updated_at FROM interfaces WHERE device_id=?", (device_id,))
    else:
        cursor.execute("SELECT id, device_id, name, mac, ip, status, description, updated_at FROM interfaces")
    rows = cursor.fetchall()
    conn.close()

    print("\n=== INTERFACES ===")
    print(tabulate(rows, headers=["ID", "DeviceID", "Name", "MAC", "IP", "Status", "Description", "Updated"], tablefmt="pretty"))


def view_logs(device_id=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if device_id:
        cursor.execute("SELECT id, device_id, command, output, executed_at FROM logs WHERE device_id=?", (device_id,))
    else:
        cursor.execute("SELECT id, device_id, command, output, executed_at FROM logs")
    rows = cursor.fetchall()
    conn.close()

    print("\n=== LOGS ===")
    print(tabulate(rows, headers=["ID", "DeviceID", "Command", "Output", "Executed"], tablefmt="pretty"))


if __name__ == "__main__":
    print("📊 Network Inventory Viewer")
    view_devices()
    view_interfaces()
    view_logs()
