# network_project/inventory_manager/main_inventory_manager.py


import yaml
import os

DEVICES_FILE = "inventory_manager/devices.yaml"

# ---------------------------
# Funciones para manejar YAML
# ---------------------------
def load_devices():
    if not os.path.exists(DEVICES_FILE):
        return {"devices": []}
    with open(DEVICES_FILE, "r") as f:
        data = yaml.safe_load(f)
        if data is None:
            return {"devices": []}
        return data

def save_devices(data):
    with open(DEVICES_FILE, "w") as f:
        yaml.safe_dump(data, f)

# ---------------------------
# Elegir tipo de dispositivo
# ---------------------------
def choose_device_type():
    tipos = ["router", "switch"]
    print("\nSelecciona el tipo de dispositivo:")
    for i, t in enumerate(tipos, 1):
        print(f"{i}. {t}")
    while True:
        choice = input("Ingresa el número: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(tipos):
                return tipos[index]
            else:
                print("❌ Número inválido, intenta de nuevo.")
        except ValueError:
            print("❌ Ingresa un número válido.")

# ---------------------------
# CRUD completo
# ---------------------------
def add_device():
    print("\n=== ➕ Agregar nuevo dispositivo ===")
    name = input("Nombre del dispositivo: ")
    ip = input("IP de gestión: ")
    dev_type = choose_device_type()
    username = input("Usuario: ")
    password = input("Contraseña: ")

    device = {
        "name": name,
        "ip": ip,
        "type": dev_type,
        "username": username,
        "password": password
    }

    data = load_devices()
    data["devices"].append(device)
    save_devices(data)
    print(f"✅ Dispositivo {name} agregado correctamente.")

def update_device():
    data = load_devices()
    devices = data.get("devices", [])
    if not devices:
        print("⚠️ No hay dispositivos para actualizar.")
        return

    print("\nDispositivos disponibles:")
    for i, dev in enumerate(devices, 1):
        print(f"{i}. {dev['name']} ({dev['type']}) - {dev['ip']}")
    sel = input("Selecciona el número del dispositivo a actualizar: ")
    try:
        sel_index = int(sel) - 1
        if sel_index < 0 or sel_index >= len(devices):
            raise ValueError
    except ValueError:
        print("❌ Selección inválida.")
        return

    device = devices[sel_index]
    print(f"\nActualizando {device['name']} (dejar vacío para no cambiar)")

    name = input(f"Nombre [{device['name']}]: ") or device['name']
    ip = input(f"IP [{device['ip']}]: ") or device['ip']
    
    print("\nSelecciona el tipo de dispositivo:")
    dev_type = choose_device_type() or device['type']  # aunque siempre selecciona, se mantiene por si quieres ajustar

    username = input(f"Usuario [{device['username']}]: ") or device['username']
    password = input(f"Contraseña [{device['password']}]: ") or device['password']

    devices[sel_index] = {
        "name": name,
        "ip": ip,
        "type": dev_type,
        "username": username,
        "password": password
    }

    save_devices(data)
    print(f"✅ Dispositivo {name} actualizado correctamente.")


def delete_device():
    data = load_devices()
    devices = data.get("devices", [])
    if not devices:
        print("⚠️ No hay dispositivos para eliminar.")
        return

    print("\nDispositivos disponibles:")
    for i, dev in enumerate(devices, 1):
        print(f"{i}. {dev['name']} ({dev['type']}) - {dev['ip']}")
    print("0. Volver al menú sin eliminar")

    sel = input("Selecciona el número del dispositivo a eliminar: ")
    if sel == "0":
        print("↩️ Volviendo al menú de gestión...")
        return

    try:
        sel_index = int(sel) - 1
        if sel_index < 0 or sel_index >= len(devices):
            raise ValueError
    except ValueError:
        print("❌ Selección inválida.")
        return

    removed = devices.pop(sel_index)
    save_devices(data)
    print(f"✅ Dispositivo {removed['name']} eliminado correctamente.")


def list_devices():
    data = load_devices()
    devices = data.get("devices", [])
    if not devices:
        print("⚠️ No hay dispositivos en el inventario.")
        return
    print("\n=== 📋 Dispositivos en inventario ===")
    for i, dev in enumerate(devices, 1):
        print(f"{i}. {dev['name']} ({dev['type']}) - {dev['ip']}")

# ---------------------------
# Menú de Gestión de Dispositivos
# ---------------------------
def manage_devices():
    while True:
        print("\n=== 📂 Gestión de Dispositivos ===")
        print("1. Agregar dispositivo")
        print("2. Actualizar dispositivo existente")
        print("3. Eliminar dispositivo")
        print("4. Listar dispositivos")
        print("0. Volver al menú principal")
        choice = input("Selecciona una opción: ")
        if choice == "1":
            add_device()
        elif choice == "2":
            update_device()
        elif choice == "3":
            delete_device()
        elif choice == "4":
            list_devices()
        elif choice == "0":
            break
        else:
            print("❌ Opción inválida.")

# Permitir ejecutar el módulo directamente
if __name__ == "__main__":
    manage_devices()
