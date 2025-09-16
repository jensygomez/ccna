# NetMonDB/core/ssh_connector/main_ssh_connector.py


# core/ssh_connector/main_ssh_connector.py
from .ssh_ssh_connector import connect_and_get_running_config

def ssh_main(device_info):
    """
    Función principal de SSH Connector
    Recibe device_info como dict y devuelve el show running-config
    """
    output = connect_and_get_running_config(
        ip=device_info['ip'],
        username=device_info['username'],
        password=device_info['password']
    )
    return output
