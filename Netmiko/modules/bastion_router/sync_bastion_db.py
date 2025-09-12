import sqlite3
from modules.database_manager.db_utils import init_db, add_device, add_interface
from .connect_bastion import connect_to_bastion

# Ruta de la base de datos (misma que en db_utils)
DB_PATH = "modules/database/net_devices.db"

def sync_bastion_interfaces(device_name="Bastion", device_ip="192.168.18.110", device_mac=None, model="ISR4331", location="Home Lab"):
    """
    Conecta al Bastion, obtiene las interfaces y actualiza la DB.
    """
    # Inicializa DB si no existe
    init_db()

    # Registrar el dispositivo (si ya existe, devuelve el device_id existente)
    device_id = add_device(device_name, "Router", device_ip, device_mac, model, location)

    # Conectarse al Bastion y obtener interfaces
    output = connect_to_bastion()
    if not output:
        print("❌ Could not retrieve interfaces from Bastion.")
        return

    # Procesar cada línea de show ip interface brief
    lines = output.splitlines()
    for line in lines[1:]:  # saltamos header
        parts = line.split()
        if len(parts) < 6:
            continue
        name, ip, ok, method, status, protocol = parts[:6]
        # Insertar o actualizar la interfaz en la base de datos
        add_interface(device_id, name=name, ip=ip, status=status, description="", mac=None)

    print("✅ Interfaces synced with the database.")


if __name__ == "__main__":
    sync_bastion_interfaces()
