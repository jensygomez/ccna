#Netmiko/main_netmiko.py
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
    
    # Opcional: Limpiar duplicados existentes (descomenta si quieres usarlo)
    # db_utils.clean_duplicate_devices()
    
    mostrar_resumen_db()
    
    # Obtener credenciales del Bastion
    creds = db_utils.get_bastion_credentials()
    if not creds:
        print("⚠ No se encontraron credenciales del Bastion. Escaneando...")
        device_id = db_utils.add_or_update_bastion(
            "192.168.18.110", 
            "bastion", 
            "bastion", 
            "bastion"  # Added secret parameter
        )
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
        print("❌ No se pudo conectar al Bastion. Saliendo...")
        return
    
    # Obtener vecinos LLDP
    neighbors = bastion.get_lldp_neighbors()
    
    print(f"🔍 Encontrados {len(neighbors)} vecinos LLDP")
    
    for n in neighbors:
        # Mejorar el nombre si es "N/A"
        device_name = n["neighbor_name"]
        if device_name == "N/A" and n.get("neighbor_ip"):
            device_name = f"Device-{n['neighbor_ip']}"
        elif device_name == "N/A":
            device_name = f"Unknown-{n['neighbor_port']}"
        
        # Determinar tipo basado en capabilities
        device_type = "Switch"  # Por defecto
        if n.get("neighbor_type"):
            if "Router" in n["neighbor_type"]:
                device_type = "Router"
            elif "Bridge" in n["neighbor_type"]:
                device_type = "Bridge"
        
        # Primero agregar o actualizar el vecino en devices
        neighbor_device_id = db_utils.add_or_update_device(
            name=device_name,
            type_=device_type,
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