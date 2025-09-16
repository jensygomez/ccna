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
        "password": password,
        "extra": edit_nested_fields()  # campos dinámicos
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
    sel_index = int(input("Selecciona el número del dispositivo a actualizar: ")) - 1
    device = devices[sel_index]

    # Campos básicos con opción de mantener
    name = input(f"Nombre [{device['name']}]: ") or device['name']
    ip = input(f"IP [{device['ip']}]: ") or device['ip']
    username = input(f"Usuario [{device['username']}]: ") or device['username']
    password = input(f"Contraseña [{device['password']}]: ") or device['password']

    # Tipo de dispositivo
    tipos = ["router", "switch"]
    print("\nSelecciona el tipo de dispositivo (Enter para no cambiar):")
    for i, t in enumerate(tipos, 1):
        print(f"{i}. {t} {'(actual)' if t == device['type'] else ''}")
    choice = input("Ingresa el número: ")
    dev_type = device['type']  # por defecto
    if choice.strip() != "":
        index = int(choice) - 1
        if 0 <= index < len(tipos):
            dev_type = tipos[index]

    # Campos dinámicos jerárquicos
    extra = edit_nested_fields(existing_extra=device.get('extra', {}))

    # Guardar cambios
    devices[sel_index] = {
        "name": name,
        "ip": ip,
        "type": dev_type,
        "username": username,
        "password": password,
        "extra": extra
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


def edit_nested_fields(existing_extra=None):
    """
    existing_extra: diccionario con los campos extra ya existentes
    """
    extra = existing_extra.copy() if existing_extra else {}

    while True:
        key = input("\nCampo a agregar/editar (interfaces, vlans, rutas...) [Enter para terminar]: ").strip()
        if key == "":
            break

        items = extra.get(key, [])

        while True:
            print(f"\n--- Editando campo '{key}' ---")
            item = {}
            # Si ya hay elementos existentes, preguntar si queremos editarlos
            if items:
                for i, old_item in enumerate(items, 1):
                    print(f"\nElemento existente #{i}: {old_item}")
                    for attr, value in old_item.items():
                        new_val = input(f"{attr} [{value}]: ").strip()
                        item[attr] = new_val if new_val != "" else value
                    # Reemplazamos elemento existente
                    items[i-1] = item
                edit_more = input("¿Agregar otro elemento a este campo? (s/n): ").lower()
                if edit_more != "s":
                    break
            else:
                while True:
                    attr = input("Atributo (nombre, ip, status...) [Enter para terminar este elemento]: ").strip()
                    if attr == "":
                        break
                    value = input(f"Valor de '{attr}': ").strip()
                    item[attr] = value
                if not item:
                    break
                items.append(item)
                more = input("Agregar otro elemento a este campo? (s/n): ").lower()
                if more != "s":
                    break

        if items:
            extra[key] = items

    return extra



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
