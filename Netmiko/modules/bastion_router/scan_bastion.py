#Netmiko/modules/bastion_router/scan_bastion.pyfrom netmiko import ConnectHandler
from modules.database_manager import db_utils

def scan_and_save_bastion(host, username, password, secret):
    """
    Conecta al Bastion y guarda sus credenciales en la DB si no existen,
    o las actualiza si ya están.
    """
    bastion_data = {
        "name": "Bastion",
        "host": host,
        "username": username,
        "password": password,
        "secret": secret,
        "type_": "cisco_ios",
    }

    # Intentamos guardar en DB
    db_utils.add_or_update_bastion(bastion_data)
    print("✅ Bastion escaneado y guardado/actualizado en la base de datos.")
