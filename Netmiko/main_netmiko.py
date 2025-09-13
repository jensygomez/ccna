# Netmiko/main_netmiko.py
from modules.bastion_router.connect_bastion import BastionManager
from modules.database_manager import db_utils
from datetime import datetime

def mostrar_resumen_db():
    devices = db_utils.get_devices()
    if not devices:
        print("📂 No hay dispositivos en la base de datos.\n")
        return
    
    print("📊 Resumen de la base de datos:\n")
    for d in devices:
        print(f" - ID: {d[0]}, Name: {d[1]}, Type: {d[2]}, IP: {d[3]}, MAC: {d[4]}, Model: {d[5]}, Location: {d[6]}, Registered: {d[7]}")
    print("")  # línea en blanco al final

def main():
    print("🔹 Iniciando Network Manager...\n")
    
    # Inicializar DB
    db_utils.init_db()

    # Mostrar estado actual de la DB
    mostrar_resumen_db()

    # Obtener credenciales del Bastion
    creds = db_utils.get_bastion_credentials()
    if not creds:
        print("⚠ No se encontraron credenciales del Bastion. Escaneando...")
        device_id = db_utils.add_or_update_bastion("192.168.18.110", "bastion", "bastion")
        creds = db_utils.get_bastion_credentials()
        print("✅ Bastion escaneado y guardado/actualizado en la base de datos.")

    # Conectarse al Bastion
    bastion = BastionManager(
        host=creds["host"],
        username=creds["username"],
        password=creds["password"],
        secret=creds["secret"]
    )
    bastion.connect()

    # Obtener vecinos LLDP
    neighbors = bastion.get_lldp_neighbors()
    device_id = creds["device_id"]
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
    print("✅ Escaneo LLDP completado y sincronizado con la base de datos.\n")

    # Mostrar resumen final después del escaneo
    mostrar_resumen_db()

if __name__ == "__main__":
    main()
