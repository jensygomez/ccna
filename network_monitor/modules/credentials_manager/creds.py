# network_monitor/modules/credentials_manager/creds.py
# Importamos las funciones necesarias desde database.py
from modules.db_manager.database import get_credentials, save_device_and_credentials

def request_credentials(ip):
    """Devuelve credenciales para un dispositivo, ya sea desde DB o pidiéndolas al usuario."""
    creds = get_credentials(ip)
    if creds:
        username, password = creds
        print(f"✅ Credenciales encontradas en DB para {ip}")
    else:
        username = input(f"Ingrese el usuario para {ip}: ").strip()
        password = input(f"Ingrese la contraseña para {ip}: ").strip()
        # Guardamos en DB para la próxima vez
        save_device_and_credentials(ip, hostname="unknown", mac="unknown", username=username, password=password)
    return username, password
