# modules/bastion_router/sync_bastion_db.py
from .connect_bastion import connect_to_bastion
from modules.database_manager.db_utils import (
    init_db, add_or_update_device, add_or_update_interface, add_log
)

import sqlite3
import os

DB_PATH = os.path.join("modules", "database", "net_devices.db")

def sync_bastion():
    print("🔹 Sincronizando Bastion con DB...")

    # Inicializamos la DB
    init_db()

    # Aseguramos que Bastion esté en la tabla devices
    device_id = add_or_update_device(
        name="Bastion",
        type_="Router",
        ip="192.168.18.110",
        mac="N/A",
        model="ISR4331",
        location="Home Lab"
    )

    # Obtenemos interfaces del Bastion
    interfaces = connect_to_bastion()
    if not interfaces:
        print("❌ No se pudieron obtener interfaces.")
        return

    # Recorremos interfaces y actualizamos/insertamos en DB
    for intf in interfaces:
        name, ip, mac, status = intf["name"], intf["ip"], intf["mac"], intf["status"]

        # Usamos la función moderna que ya maneja update o insert
        add_or_update_interface(
            device_id=device_id,
            name=name,
            mac=mac,
            ip=ip,
            status=status,
            description=""
        )

        # Registramos log
        add_log(device_id, f"Sync {name}", f"IP={ip}, MAC={mac}, STATUS={status}")

    print("✅ Sincronización completada.")

if __name__ == "__main__":
    sync_bastion()
