# NetMonDB/core/utils/main_utils.py

import os
import json

def register_device():
    print("📌 No se encontraron dispositivos en la base de datos.")
    print("Vamos a registrar un nuevo dispositivo...")
    hostname = input("Nombre del dispositivo: ")
    ip = input("IP del dispositivo: ")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    device_type = input("Tipo de dispositivo (ej: cisco_ios): ")

    print("\n⚙️ Configuración mínima para pegar en el dispositivo vía consola:")
    print(f"interface vlan 1\n ip address {ip} 255.255.255.0\n no shutdown\n")
    print("Asegúrate de que el dispositivo tenga SSH habilitado.\n")

    device_info = {
        "hostname": hostname,
        "ip": ip,
        "username": username,
        "password": password,
        "device_type": device_type
    }

    return device_info

def save_json_output(device_info, parsed_data):
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    filename = f"outputs/{device_info['hostname']}_running_config.json"
    with open(filename, "w") as f:
        json.dump(parsed_data, f, indent=4)
    print(f"✅ JSON guardado en {filename}")

# main opcional para probar las funciones del módulo utils
def main():
    print("🛠️ Probando funciones de utils")
    device = register_device()
    sample_data = {"test": "valor"}
    save_json_output(device, sample_data)

if __name__ == "__main__":
    main()
