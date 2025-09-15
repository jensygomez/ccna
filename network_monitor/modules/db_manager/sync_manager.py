# network_monitor/modules/db_manager/sync_manager.py

from modules.db_manager.database import get_all_devices, get_credentials, save_interfaces
from modules.parsers.interfaces import parse_interfaces
from modules.ssh_manager.ssh_handler import connect_and_run

def sync_all_devices():
    """Actualiza todas las interfaces de todos los dispositivos registrados"""
    devices = get_all_devices()
    if not devices:
        print("No hay dispositivos para sincronizar.")
        return

    print("🔄 Sincronizando todos los dispositivos...\n")
    for dev in devices:
        hostname, ip = dev[1], dev[2]
        creds = get_credentials(ip)
        if not creds:
            print(f"❌ No se encontraron credenciales para {hostname} ({ip})")
            continue
        username, password = creds
        try:
            output = connect_and_run(ip, username, password, command="show ip interface brief")
            interfaces = parse_interfaces(output)
            save_interfaces(ip, interfaces)
            print(f"✅ {hostname} ({ip}) sincronizado correctamente")
        except Exception as e:
            print(f"❌ Error al sincronizar {hostname} ({ip}): {e}")
