
#Netmiko/main_netmiko.py

from modules.scanner.network_scanner import scan_network
from modules.database_manager import db_utils

def main():
    print("🔹 Iniciando Network Manager...\n")

    # Escaneo de red
    devices = scan_network("192.168.0.0/24")

    print("\n📂 Comparando con la base de datos...")
    for dev in devices:
        db_utils.insert_or_update_device(
            name=f"Device-{dev['ip']}",  # nombre temporal
            ip=dev['ip'],
            mac=dev['mac'],
            device_type="Unknown"        # luego lo refinamos con modelo/CDP/LLDP
        )

    # Mostrar resumen actualizado
    print("\n📊 Resumen en DB:")
    all_devices = db_utils.get_all_devices()
    for d in all_devices:
        print(f" - ID: {d[0]}, Name: {d[1]}, IP: {d[2]}, MAC: {d[3]}, Type: {d[4]}")

if __name__ == "__main__":
    main()
