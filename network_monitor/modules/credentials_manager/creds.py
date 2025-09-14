# network_monitor/modules/credentials_manager/creds.py
from modules.db_manager.database import get_credentials, save_device_and_credentials

def request_credentials(ip, hostname=None, mac=None):
    """Obtiene credenciales de la DB, si no existen las pide al usuario."""
    creds = get_credentials(ip)
    if creds:
        print(f"✅ Credenciales encontradas en DB para {ip}")
        return creds
    else:
        print(f"⚠️ No hay credenciales guardadas para {ip}")
        username = input("Ingrese el usuario: ").strip()
        password = input("Ingrese la contraseña: ").strip()

        save_device_and_credentials(ip, hostname or "unknown", mac or "unknown", username, password)
        return username, password
