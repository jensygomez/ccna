# modules/parsers/device_info.py

# network_monitor/modules/parsers/device_info.py
import re
from modules.db_manager.database import save_device_and_credentials, show_device_summary

def parse_hostname(show_version_output):
    """
    Extrae el hostname del dispositivo desde show version.
    Nota: Si el hostname no está en show version, se podría usar otro comando,
    o inicializarlo con la configuración base.
    """
    # Buscamos una línea tipo 'hostname Bastion' si está en la config
    match = re.search(r"hostname (\S+)", show_version_output, re.IGNORECASE)
    if match:
        return match.group(1)
    # fallback
    return "unknown"

def parse_mac(show_version_output):
    """
    Extrae la MAC del procesador o del dispositivo desde show version.
    Puede variar según el modelo, muchas veces es el 'Processor board ID'.
    """
    match = re.search(r"Processor board ID (\S+)", show_version_output, re.IGNORECASE)
    if match:
        return match.group(1)
    return "unknown"

def save_device_info(ip, hostname, mac, username=None, password=None):
    """
    Guarda en la base de datos la información del dispositivo y opcionalmente credenciales.
    """
    if username and password:
        save_device_and_credentials(ip, hostname, mac, username, password)
    else:
        # Si no hay credenciales, solo guarda IP, hostname y MAC
        save_device_and_credentials(ip, hostname, mac, "", "")
    
    # Mostrar resumen
    show_device_summary(ip)
