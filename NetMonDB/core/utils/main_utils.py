# NetMonDB/core/utils/main_utils.py

# core/utils/main_utils.py
# core/utils/main_utils.py
import os
import json

def expand_interface(abbrev):
    """
    Convierte abreviaturas de interfaz a forma completa.
    """
    abbrev = abbrev.lower()
    if abbrev.startswith("g"):
        return "GigabitEthernet" + abbrev[1:]
    elif abbrev.startswith("e"):
        return "Ethernet" + abbrev[1:]
    elif abbrev.startswith("f"):
        return "FastEthernet" + abbrev[1:]
    else:
        return abbrev  # si ya es completo, lo devuelve tal cual

def register_device():
    print("📌 No se encontraron dispositivos en la base de datos.")
    print("Vamos a registrar un nuevo dispositivo...")
    hostname = input("Nombre del dispositivo: ")
    ip = input("IP del dispositivo: ")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    gateway = input("Puerta de enlace (gateway): ")
    interface_abbrev = input("Interfaz para configurar IP (ej: g0/0, e0/0): ")
    interface = expand_interface(interface_abbrev)

    print("\n⚙️ Configuración completa para pegar en el dispositivo vía consola:\n")
    config_lines = [
        "configure terminal",
        f"hostname {hostname}",
        "lldp run",
        f"interface {interface}",
        f" ip address {ip} 255.255.255.0",
        " no shutdown",
        f"ip route 0.0.0.0 0.0.0.0 {gateway}",
        "ip domain-name lab.local",
        "crypto key generate rsa modulus 1024",
        "ip ssh version 2",
        "line vty 0 4",
        " login local",
        " transport input telnet ssh",
        f"username {username} privilege 15 secret {password}",
        f"enable secret {password}",
        "end",
        "write memory"
    ]

    for line in config_lines:
        print(line)

    print("\n✅ Copia y pega esta configuración en el dispositivo y asegúrate que SSH esté activo.\n")

    device_info = {
        "hostname": hostname,
        "ip": ip,
        "username": username,
        "password": password,
        "gateway": gateway,
        "interface": interface
    }

    return device_info

def save_json_output(device_info, parsed_data):
    """
    Guarda la información parseada en un archivo JSON dentro de outputs/
    """
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    filename = f"outputs/{device_info['hostname']}_running_config.json"
    with open(filename, "w") as f:
        json.dump(parsed_data, f, indent=4)
    print(f"✅ JSON guardado en {filename}")
