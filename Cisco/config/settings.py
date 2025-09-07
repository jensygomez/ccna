"""
Configuración de la aplicación
"""

# Configuración de dispositivos
DEVICES = {
    'switch1': {
        'device_type': 'cisco_ios',
        'host': '192.168.1.1',
        'username': 'admin',
        'password': 'password',
        'secret': 'enable',
        'port': 22,
    }
}

# Configuración de la aplicación
APP_CONFIG = {
    'timeout': 10,
    'delay_factor': 1,
}
