#Netmiko/main_netmiko.py
from modules.bastion_router.connect_bastion import BastionManager
from modules.database_manager import db_utils
from datetime import datetime

def mostrar_resumen_db():
    devices = db_utils.get_devices()
    print("\n📊 Resumen de la base de datos:\n")
    if not devices:
        print("No hay dispositivos registrados.\n")
    else:
        print(f"Total de dispositivos: {len(devices)}")
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
        print("⚠ No se encontraron credenciales del Bastion. Configurando...")
        device_id = db_utils.add_or_update_bastion(
            "192.168.18.110", 
            "bastion", 
            "bastion", 
            "bastion"
        )
        if device_id:
            creds = db_utils.get_bastion_credentials()
            print("✅ Bastion configurado en la base de datos.")
        else:
            print("❌ Error al configurar Bastion. Saliendo...")
            return
    
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
    print("🔍 Obteniendo vecinos LLDP...")
    neighbors = bastion.get_lldp_neighbors()
    
    print(f"✅ Encontrados {len(neighbors)} vecinos LLDP")
    
    for i, n in enumerate(neighbors, 1):
        print(f"  Procesando vecino {i}/{len(neighbors)}...")
        
        # Mejorar el nombre si es "N/A"
        device_name = n["neighbor_name"]
        device_ip = n.get("neighbor_ip")
        
        if device_name == "N/A" or not device_name:
            if device_ip:
                device_name = f"Device-{device_ip}"
            else:
                device_name = f"Unknown-{n['neighbor_port']}"
        
        # Determinar tipo basado en capabilities
        device_type = "Switch"  # Por defecto
        capabilities = n.get("neighbor_type", "")
        if capabilities:
            if "Router" in capabilities:
                device_type = "Router"
            elif "Bridge" in capabilities:
                device_type = "Bridge"
        
        # Buscar dispositivo existente usando la nueva función robusta
        existing_device_id = db_utils.find_device_by_identifiers(
            name=device_name,
            ip=device_ip,
            mac=None  # Podrías agregar MAC si la obtienes del LLDP
        )
        
        if existing_device_id:
            # Usar dispositivo existente
            neighbor_device_id = existing_device_id
            print(f"    🔄 Usando dispositivo existente ID: {existing_device_id}")
        else:
            # Agregar nuevo dispositivo
            neighbor_device_id = db_utils.add_or_update_device(
                name=device_name,
                type_=device_type,
                ip=device_ip,
                mac=None,
                model=n.get("neighbor_model"),
                location=None
            )
            if neighbor_device_id:
                print(f"    ➕ Nuevo dispositivo ID: {neighbor_device_id}")
            else:
                print(f"    ⚠ No se pudo agregar dispositivo: {device_name}")
                continue
        
        # Agregar información LLDP
        db_utils.add_or_update_lldp_neighbor(
            device_id=neighbor_device_id,
            local_interface=n["local_intf"],
            neighbor_name=n["neighbor_name"],
            neighbor_port=n["neighbor_port"],
            neighbor_ip=device_ip,
            neighbor_type=n.get("neighbor_type"),
            neighbor_model=n.get("neighbor_model")
        )
    
    bastion.disconnect()
    
    print("✅ Escaneo LLDP completado y sincronizado con la base de datos.")
    
    # Mostrar resumen final
    mostrar_resumen_db()

if __name__ == "__main__":
    main()