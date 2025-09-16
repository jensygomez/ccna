# network_project/inventory_manager/main_inventory_manager.py

import os
from tabulate import tabulate
from inventory_manager import db_manager

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
# CRUD Dispositivos
# ---------------------------
def add_device():
    print("\n=== ➕ Agregar nuevo dispositivo ===")
    name = input("Nombre del dispositivo: ")
    ip = input("IP de gestión: ")
    dev_type = choose_device_type()
    username = input("Usuario: ")
    password = input("Contraseña: ")

    db_manager.add_device(name, dev_type, ip, username, password)
    print(f"✅ Dispositivo {name} agregado correctamente.")

def list_devices():
    devices = db_manager.list_devices()
    if not devices:
        print("⚠️ No hay dispositivos en inventario.")
        return
    table = [["#", "Name", "Type", "IP Gestión", "Username", "Password"]]
    for idx, d in enumerate(devices, 1):
        table.append([idx, d[1], d[2], d[3], d[4], d[5]])
    print("\n=== 📋 Dispositivos en inventario ===")
    print(tabulate(table, headers="firstrow", tablefmt="grid"))

def update_device():
    devices = db_manager.list_devices()
    if not devices:
        print("⚠️ No hay dispositivos para actualizar.")
        return

    list_devices()
    sel = input("Selecciona el número del dispositivo a actualizar: ")
    try:
        sel_index = int(sel) - 1
        if sel_index < 0 or sel_index >= len(devices):
            raise ValueError
    except ValueError:
        print("❌ Selección inválida.")
        return

    device = devices[sel_index]
    device_id = device[0]
    updated_fields = {}

    print(f"\nEditando dispositivo {device[1]} (dejar vacío para no cambiar):")
    new_name = input(f"Nombre [{device[1]}]: ").strip()
    if new_name:
        updated_fields["name"] = new_name
    new_ip = input(f"IP Gestión [{device[3]}]: ").strip()
    if new_ip:
        updated_fields["ip_management"] = new_ip
    new_user = input(f"Username [{device[4]}]: ").strip()
    if new_user:
        updated_fields["username"] = new_user
    new_pass = input(f"Password [{device[5]}]: ").strip()
    if new_pass:
        updated_fields["password"] = new_pass

    # Tipo de dispositivo
    print(f"Tipo actual: {device[2]}")
    change_type = input("Cambiar tipo de dispositivo? (s/n): ").lower()
    if change_type == "s":
        updated_fields["type"] = choose_device_type()

    if updated_fields:
        db_manager.update_device(device_id, **updated_fields)
        print(f"✅ Dispositivo {device[1]} actualizado correctamente.")
    else:
        print("⚠️ No se realizaron cambios.")

def delete_device():
    devices = db_manager.list_devices()
    if not devices:
        print("⚠️ No hay dispositivos para eliminar.")
        return

    list_devices()
    sel = input("Selecciona el número del dispositivo a eliminar (0 para cancelar): ")
    if sel == "0":
        print("↩️ Cancelado.")
        return

    try:
        sel_index = int(sel) - 1
        if sel_index < 0 or sel_index >= len(devices):
            raise ValueError
    except ValueError:
        print("❌ Selección inválida.")
        return

    device = devices[sel_index]
    db_manager.delete_device(device[0])
    print(f"✅ Dispositivo {device[1]} eliminado correctamente.")

# ---------------------------
# CRUD Interfaces
# ---------------------------
def manage_interfaces(device_id):
    while True:
        interfaces = db_manager.list_interfaces(device_id)
        print("\n=== Interfaces del dispositivo ===")
        if interfaces:
            table = [["#", "Name", "IP", "Status", "Mode", "Description"]]
            for idx, iface in enumerate(interfaces, 1):
                table.append([idx, iface[2], iface[3], iface[4], iface[5], iface[6]])
            print(tabulate(table, headers="firstrow", tablefmt="grid"))
        else:
            print("⚠️ No hay interfaces registradas.")

        print("\nOpciones:")
        print("1. Agregar Interface")
        print("0. Volver")
        choice = input("Selecciona una opción: ").strip()
        if choice == "0":
            break
        elif choice == "1":
            name = input("Nombre Interface (g0/0,...): ")
            ip = input("IP: ")
            status = input("Status (UP/DOWN): ")
            mode = input("Mode (trunk/access): ")
            desc = input("Descripción: ")
            db_manager.add_interface(device_id, name, ip, status, mode, desc)
            print(f"✅ Interface {name} agregada correctamente.")
        else:
            print("❌ Opción inválida.")

# ---------------------------
# Menú principal
# ---------------------------
def manage_devices_menu():
    while True:
        print("\n=== 📂 Gestión de Dispositivos ===")
        print("1. Agregar dispositivo")
        print("2. Actualizar dispositivo existente")
        print("3. Eliminar dispositivo")
        print("4. Listar dispositivos")
        print("5. Gestionar Interfaces")
        print("0. Volver al menú principal")
        choice = input("Selecciona una opción: ").strip()
        if choice == "1":
            add_device()
        elif choice == "2":
            update_device()
        elif choice == "3":
            delete_device()
        elif choice == "4":
            list_devices()
        elif choice == "5":
            devices = db_manager.list_devices()
            list_devices()
            sel = input("Selecciona el número del dispositivo para gestionar interfaces: ")
            try:
                sel_index = int(sel) - 1
                if sel_index < 0 or sel_index >= len(devices):
                    raise ValueError
                manage_interfaces(devices[sel_index][0])
            except ValueError:
                print("❌ Selección inválida.")
        elif choice == "0":
            break
        else:
            print("❌ Opción inválida.")

# ---------------------------
# Ejecutar módulo directamente
# ---------------------------
if __name__ == "__main__":
    manage_devices_menu()
