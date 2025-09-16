# network_project/inventory_manager/main_inventory_manager.py


import yaml
import os
from tabulate import tabulate  # <- aquí
from inventory_manager.inventory_utils import mostrar_dispositivos





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








def edit_interfaces(interfaces):
    """
    Edita o agrega interfaces, busca por nombre.
    """
    while True:
        if interfaces:
            print("\nInterfaces actuales:")
            for i, iface in enumerate(interfaces, 1):
                print(f"{i}. {iface}")
        else:
            print("\nNo hay interfaces registradas.")

        action = input("Agregar/Editar Interface? (a/e, Enter para salir): ").lower()
        if action == "":
            break
        elif action == "a":
            iface_name = input("Nombre Interface (g0/0,...): ")
            ip = input("IP: ")
            status = input("Status (UP/DOWN): ")
            mode = input("Mode (trunk/access): ")
            interfaces.append({"Interface": iface_name, "IP": ip, "status": status, "mode": mode})
        elif action == "e":
            search_name = input("Nombre de la Interface a editar: ").strip()
            # Buscar la interfaz por nombre
            found = False
            for iface in interfaces:
                if iface.get("Interface") == search_name:
                    found = True
                    iface['IP'] = input(f"IP [{iface.get('IP','')}]: ") or iface.get('IP','')
                    iface['status'] = input(f"Status [{iface.get('status','')}]: ") or iface.get('status','')
                    iface['mode'] = input(f"Mode [{iface.get('mode','')}]: ") or iface.get('mode','')
                    break
            if not found:
                print("❌ No se encontró esa interfaz.")
        else:
            print("❌ Opción inválida.")
    return interfaces



def update_device():
    data = load_devices()
    devices = data.get("devices", [])
    if not devices:
        print("⚠️ No hay dispositivos para actualizar.")
        return

    mostrar_dispositivos({d['name']: d for d in devices})

    sel = input("Selecciona el número del dispositivo a actualizar: ")
    try:
        sel_index = int(sel) - 1
        if sel_index < 0 or sel_index >= len(devices):
            raise ValueError
    except ValueError:
        print("❌ Selección inválida.")
        return

    device = devices[sel_index]
    extra = device.get("extra", {})

    while True:
        # Construir tabla resumen del dispositivo
        table = [["Atributo", "Valor"]]
        table.append(["Nombre", device['name']])
        table.append(["IP Gestión", device['ip']])
        table.append(["Usuario", device['username']])
        table.append(["Contraseña", device['password']])
        table.append(["Tipo", device['type']])
        for key, items in extra.items():
            val_str = ""
            for item in items:
                if isinstance(item, dict):
                    val_str += ", ".join(f"{k}={v}" for k, v in item.items()) + "\n"
                else:
                    val_str += str(item) + "\n"
            table.append([key, val_str.strip()])
        print("\n=== Información actual del dispositivo ===")
        print(tabulate(table, headers="firstrow", tablefmt="grid"))

        # Menú dinámico
        existing_keys = list(extra.keys())
        print("\n¿Qué atributo quieres actualizar o agregar?")
        for i, key in enumerate(existing_keys, 1):
            print(f"{i} - {key}")
        print(f"{len(existing_keys)+1} - Crear nuevo atributo")
        print("0 - Salir")

        choice = input("Selecciona una opción: ").strip()
        if choice == "0":
            break

        # Determinar acción
        try:
            choice_idx = int(choice) - 1
        except ValueError:
            print("❌ Entrada inválida")
            continue

        if choice_idx == len(existing_keys):
            # Crear nuevo atributo
            new_attr = input("Nombre del nuevo atributo: ").strip()
            if not new_attr:
                print("❌ Nombre vacío, cancelado")
                continue
            extra[new_attr] = edit_nested_fields()
        elif 0 <= choice_idx < len(existing_keys):
            # Editar atributo existente
            attr_key = existing_keys[choice_idx]
            if attr_key.lower() == "interfaces":
                interfaces = extra.get("interfaces", [])
                interfaces = edit_interfaces(interfaces)
                extra["interfaces"] = interfaces
            else:
                items = extra.get(attr_key, [])
                items = edit_nested_fields(items)
                extra[attr_key] = items
        else:
            print("❌ Opción inválida.")

    device['extra'] = extra
    devices[sel_index] = device
    save_devices(data)
    print(f"✅ Dispositivo {device['name']} actualizado correctamente.")






def delete_device():
    data = load_devices()
    devices = data.get("devices", [])
    if not devices:
        print("⚠️ No hay dispositivos para eliminar.")
        return


    mostrar_dispositivos(devices)
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


def edit_interfaces(existing_interfaces=None):
    """
    existing_interfaces: lista de diccionarios con interfaces actuales
    """
    interfaces = existing_interfaces.copy() if existing_interfaces else []

    while True:
        if interfaces:
            print("\nInterfaces actuales:")
            for intf in interfaces:
                name = intf.get("Interface", "N/A")
                attrs = ", ".join(f"{k}={v}" for k, v in intf.items() if k != "Interface")
                print(f"- {name}: {attrs}")
        else:
            print("\nNo hay interfaces registradas.")

        choice = input("Escribe el nombre de la interfaz a editar o Enter para salir: ").strip()
        if choice == "":
            break

        # Buscar si existe
        found = None
        for intf in interfaces:
            if intf.get("Interface") == choice:
                found = intf
                break

        if found:
            print(f"\nEditando interfaz {choice} (dejar vacío para no cambiar)")
            for attr, value in found.items():
                if attr == "Interface":
                    continue
                new_val = input(f"{attr} [{value}]: ").strip()
                if new_val != "":
                    found[attr] = new_val
        else:
            print(f"\nInterfaz {choice} no encontrada. Se agregará como nueva.")
            new_intf = {"Interface": choice}
            while True:
                attr = input("Atributo (Enter para terminar este interfaz): ").strip()
                if attr == "":
                    break
                val = input(f"Valor de '{attr}': ").strip()
                new_intf[attr] = val
            interfaces.append(new_intf)

    return interfaces



# ---------------------------
# Función para listar dispositivos
# ---------------------------
def list_devices():
    data = load_devices()
    devices_list = data.get("devices", [])
    if not devices_list:
        print("⚠️ No hay dispositivos en inventario.")
        return
    devices_dict = {d['name']: d for d in devices_list}
    mostrar_dispositivos(devices_dict)




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
