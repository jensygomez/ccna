from netmiko import ConnectHandler

# Datos del switch
switch = {
    "device_type": "cisco_ios_telnet",  # para Telnet
    "host": "192.168.1.2",
    "username": "",  # si tu switch no requiere username, dejar vacío
    "password": "cisco",
    "secret": "cisco",  # contraseña enable
}

# Conectarse al switch
net_connect = ConnectHandler(**switch)

# Entrar al modo enable
net_connect.enable()

# Configuración de comandos
commands = [
    "configure terminal",
    "hostname Sucursal_01",
    "end",
    "write memory",
]

# Enviar comandos
output = net_connect.send_config_set(commands)
print(output)

# Cerrar conexión
net_connect.disconnect()

