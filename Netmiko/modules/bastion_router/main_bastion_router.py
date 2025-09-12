# modules/bastion_router/main_bastion_router.py
from .connect_bastion import connect_to_bastion
from modules.database_manager.db_utils import init_db, add_or_update_device, sync_device_interfaces

def main():
    init_db()

    # 1️⃣ Conectar al Bastion y obtener interfaces
    interfaces = connect_to_bastion()
    if not interfaces:
        print("❌ No se pudieron obtener interfaces")
        return

    # 2️⃣ Agregar o actualizar el dispositivo
    device_id = add_or_update_device(
        name="Bastion",
        type_="Router",
        ip="192.168.18.110"
    )

    # 3️⃣ Sincronizar interfaces
    sync_device_interfaces(device_id, interfaces)
    print("✅ Interfaces sincronizadas en la base de datos")
