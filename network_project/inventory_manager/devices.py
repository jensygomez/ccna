# network_project/inventory_manager/devices.py

from tabulate import tabulate
from database_manager import db_crud

# ---------------------------
# Funciones CRUD genéricas para dispositivos
# ---------------------------
def list_devices(return_list=False):
    devices = db_crud.list_all("devices")
    if not devices:
        print("⚠️ No hay dispositivos en inventario.")
        return [] if return_list else None
    table = [["#", "Nombre", "Tipo", "IP Gestión", "Usuario", "Contraseña"]]
    for idx, d in enumerate(devices, 1):
        table.append([idx, d[1], d[2], d[3], d[4], d[5]])
    print("\n=== 📋 Dispositivos en inventario ===")
    print(tabulate(table, headers="firstrow", tablefmt="grid"))
    return devices if return_list else None

def add_device():
    print("\n=== ➕ Agregar nuevo dispositivo ===")
    name = input("Nombre del dispositivo: ").strip()
    ip = input("IP de gestión: ").strip()
    dev_type = input("Tipo (router/switch): ").strip()
    username = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()
    conn = db_crud.connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO devices (name, type, ip_management, username, password) VALUES (?, ?, ?, ?, ?)",
        (name, dev_type, ip, username, password)
    )
    conn.commit()
    conn.close()
    print(f"✅ Dispositivo {name} agregado correctamente.")

def update_device():
    devices = list_devices(return_list=True)
    if not devices:
        return
    sel_idx = select_from_list([d[1] for d in devices], "Selecciona dispositivo a actualizar:")
    if sel_idx is None:
        return
    device = devices[sel_idx]
    device_id = device[0]
    updated_fields = {}
    print(f"\nEditando dispositivo {device[1]} (dejar vacío para no cambiar):")
    new_name = input(f"Nombre [{device[1]}]: ").strip()
    new_type = input(f"Tipo [{device[2]}]: ").strip()
    new_ip = input(f"IP Gestión [{device[3]}]: ").strip()
    new_user = input(f"Usuario [{device[4]}]: ").strip()
    new_pass = input(f"Contraseña [{device[5]}]: ").strip()
    if new_name:
        updated_fields["name"] = new_name
    if new_type:
        updated_fields["type"] = new_type
    if new_ip:
        updated_fields["ip_management"] = new_ip
    if new_user:
        updated_fields["username"] = new_user
    if new_pass:
        updated_fields["password"] = new_pass
    if updated_fields:
        db_crud.update_by_id("devices", device_id, **updated_fields)
        print(f"✅ Dispositivo {device[1]} actualizado correctamente.")
    else:
        print("⚠️ No se realizaron cambios.")

def delete_device():
    devices = list_devices(return_list=True)
    if not devices:
        return
    sel_idx = select_from_list([d[1] for d in devices], "Selecciona dispositivo a eliminar:")
    if sel_idx is None:
        return
    device_id = devices[sel_idx][0]
    db_crud.delete_by_id("devices", device_id)
    print(f"✅ Dispositivo {devices[sel_idx][1]} eliminado correctamente.")


# ---------------------------
# Funciones auxiliares
# ---------------------------
def select_from_list(items, prompt="Selecciona un elemento:"):
    if not items:
        print("⚠️ No hay elementos disponibles.")
        return None
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")
    sel = input(f"{prompt} ").strip()
    try:
        sel_index = int(sel) - 1
        if sel_index < 0 or sel_index >= len(items):
            raise ValueError
        return sel_index
    except ValueError:
        print("❌ Selección inválida.")
        return None


# ---------------------------
# Menú de gestión de dispositivos
# ---------------------------
def manage_devices():
    while True:
        print("\n=== 📂 Gestión de Dispositivos ===")
        print("1. Agregar dispositivo")
        print("2. Actualizar dispositivo")
        print("3. Eliminar dispositivo")
        print("4. Listar dispositivos")
        print("0. Volver")
        choice = input("Selecciona una opción: ").strip()
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
