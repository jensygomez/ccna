# Netmiko/main_netmiko.py
from modules.bastion_router.connect_bastion import BastionManager
from modules.database_manager import db_utils

def main():
    print("🔹 Iniciando Network Manager...\n")
    db_utils.init_db()

    # Obtener credenciales del Bastion desde la DB
    creds = db_utils.get_bastion_credentials()
    if not creds:
        print("⚠ No se encontraron credenciales del Bastion. Escaneando...")
        device_id = db_utils.add_or_update_bastion("192.168.18.110", "bastion", "bastion")
        creds = db_utils.get_bastion_credentials()
        print("✅ Bastion escaneado y guardado/actualizado en la base de datos.")

    # Conectar al Bastion
    bastion = BastionManager(
        host=creds["host"],
        username=creds["username"],
        password=creds["password"],
        secret=creds["secret"]
    )

    if not bastion.connect():
        print("❌ No se pudo conectar al Bastion. Terminando.")
        return

    # Obtener LLDP neighbors
    neighbors = bastion.get_lldp_neighbors()
    device_id = creds["device_id"]

    # Guardar/actualizar vecinos en la DB
    for n in neighbors:
        db_utils.add_or_update_lldp_neighbor(
            device_id=device_id,
            local_interface=n["local_intf"],
            neighbor_name=n["neighbor_name"],
            neighbor_port=n["neighbor_port"],
            neighbor_ip=n.get("neighbor_ip"),
            neighbor_type=n.get("neighbor_type"),
            neighbor_model=n.get("neighbor_model")
        )

    bastion.disconnect()
    print("✅ Escaneo LLDP completado y sincronizado con la base de datos.")

if __name__ == "__main__":
    main()
