# Netmiko/main_netmiko.py
from modules.bastion_router.connect_bastion import BastionManager
from modules.database_manager import db_utils
from datetime import datetime

def mostrar_resumen_db():
    devices = db_utils.get_devices()
    print("\n📊 Resumen de la base de datos:\n")
    if not devices:
        print("No hay dispositivos registrados.\n")
    for d in devices:
        print(f" - ID: {d[0]}, Name: {d[1]}, Type: {d[2]}, IP: {d[3]}, MAC: {d[4]}, Model: {d[5]}, Location: {d[6]}, Registered: {d[7]}")
    print()

def main():
    print("🔹 Iniciando Network Manager...\n")
    
    # Inicializar DB
    db_utils.init_db()
    mostrar_resumen_db()
    
    # Obtener credenciales del Bastion
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
    bastion.connect()
    
    # Obtener vecinos LLDP
    neighbors = bastion.get_lldp_neighbors()
    
    for n in neighbors:
        # Primero agregar o actualizar el vecino en devices
        neighbor_device_id = db_utils.add_or_update_device(
            name=n["neighbor_name"],
            type_="Switch",  # O "Router", según corresponda
            ip=n.get("neighbor_ip"),
            mac=None,
            model=n.get("neighbor_model"),
            location=None
        )
        
        # Luego agregar o actualizar LLDP
        db_utils.add_or_update_lldp_neighbor(
            device_id=neighbor_device_id,
            local_interface=n["local_intf"],
            neighbor_name=n["neighbor_name"],
            neighbor_port=n["neighbor_port"],
            neighbor_ip=n.get("neighbor_ip"),
            neighbor_type=n.get("neighbor_type"),
            neighbor_model=n.get("neighbor_model")
        )
    
    bastion.disconnect()
    
    print("✅ Escaneo LLDP completado y sincronizado con la base de datos.")
    
    # Mostrar resumen final con vecinos agregados
    mostrar_resumen_db()

if __name__ == "__main__":
    main()
