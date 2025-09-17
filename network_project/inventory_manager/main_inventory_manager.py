# network_project/inventory_manager/main_inventory_manager.py
import os
from tabulate import tabulate
from database_manager import db_crud



# Listar VLANs
vlans = db_crud.list_records("vlans")
for v in vlans:
    print(v)

# Editar VLAN
db_crud.update_record("vlans", vlan_id=1, name="VLAN-10", number=10, description="TRUNK")

# Eliminar VLAN
db_crud.delete_record("vlans", record_id=1)


# ---------------------------
# Funciones auxiliares
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

def select_from_list(items, prompt="Selecciona un elemento:"):
    if not items:
        print("⚠️ No hay elementos disponibles.")
        return None
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")
    sel = input(f"{prompt} ")
    try:
        sel_index = int(sel) - 1
        if sel_index < 0 or sel_index >= len(items):
            raise ValueError
        return sel_index
    except ValueError:
        print("❌ Selección inválida.")
        return None
    
    
    
# ---------------------------
# CRUD genérico para cualquier tabla
# ---------------------------
def edit_record(table):
    rows = db_crud.list_all(table)
    if not rows:
        print(f"⚠️ No hay registros en {table}.")
        return
    headers = [desc[0] for desc in db_crud.connect().cursor().execute(f"PRAGMA table_info({table})")]
    items = [str(row[1]) if len(row) > 1 else str(row[0]) for row in rows]
    idx = select_from_list(items, f"Selecciona un registro de {table} para editar:")
    if idx is None:
        return
    record = rows[idx]
    record_id = record[0]
    updated_fields = {}
    for i, col_name in enumerate(headers[1:], start=1):
        new_val = input(f"{col_name} [{record[i]}]: ").strip()
        if new_val:
            updated_fields[col_name] = new_val
    if updated_fields:
        db_crud.update_by_id(table, record_id, **updated_fields)
        print(f"✅ Registro de {table} actualizado correctamente.")
    else:
        print("⚠️ No se realizaron cambios.")

def delete_record(table):
    rows = db_crud.list_all(table)
    if not rows:
        print(f"⚠️ No hay registros en {table}.")
        return
    items = [str(row[1]) if len(row) > 1 else str(row[0]) for row in rows]
    idx = select_from_list(items, f"Selecciona un registro de {table} para eliminar:")
    if idx is None:
        return
    record_id = rows[idx][0]
    db_crud.delete_by_id(table, record_id)
    print(f"✅ Registro de {table} eliminado correctamente.")


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

def list_devices(return_list=False):
    devices = db_manager.list_devices()
    if not devices:
        print("⚠️ No hay dispositivos en inventario.")
        return [] if return_list else None
    table = [["#", "Name", "Type", "IP Gestión", "Username", "Password"]]
    for idx, d in enumerate(devices, 1):
        table.append([idx, d[1], d[2], d[3], d[4], d[5]])
    print("\n=== 📋 Dispositivos en inventario ===")
    print(tabulate(table, headers="firstrow", tablefmt="grid"))
    return devices if return_list else None

def update_device():
    devices = list_devices(return_list=True)
    if not devices:
        return
    sel_index = select_from_list([d[1] for d in devices], "Selecciona el dispositivo a actualizar:")
    if sel_index is None:
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
    devices = list_devices(return_list=True)
    if not devices:
        return
    sel_index = select_from_list([d[1] for d in devices], "Selecciona el dispositivo a eliminar:")
    if sel_index is None:
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
# CRUD VLANs y asignación
# ---------------------------
def manage_vlans():
    while True:
        vlans = db_manager.list_vlans()
        print("\n=== VLANs ===")
        if vlans:
            table = [["#", "Name", "Number", "Description"]]
            for idx, vlan in enumerate(vlans, 1):
                table.append([idx, vlan[1], vlan[2], vlan[3]])
            print(tabulate(table, headers="firstrow", tablefmt="grid"))
        else:
            print("⚠️ No hay VLANs registradas.")

        print("\nOpciones:")
        print("1. Agregar VLAN")
        print("2. Editar VLAN")
        print("3. Eliminar VLAN")
        print("4. Asignar VLAN a dispositivo")
        print("0. Volver")

        choice = input("Selecciona una opción: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            name = input("Nombre VLAN: ").strip()
            number = input("Número VLAN: ").strip()
            desc = input("Descripción: ").strip()
            db_manager.add_vlan(name, number, desc)
            print(f"✅ VLAN {name} agregada correctamente.")
        elif choice == "2":
            # Selecciona la VLAN a editar
            if not vlans:
                print("⚠️ No hay VLANs para editar.")
                continue
            vlan_idx = select_from_list([v[1] for v in vlans], "Selecciona VLAN a editar:")
            if vlan_idx is None:
                continue
            vlan_id = vlans[vlan_idx][0]
            current = vlans[vlan_idx]
            # Pedir nuevos valores (dejar vacío para mantener)
            new_name = input(f"Nombre [{current[1]}]: ").strip()
            new_number = input(f"Número [{current[2]}]: ").strip()
            new_desc = input(f"Descripción [{current[3]}]: ").strip()
            updated_fields = {}
            if new_name:
                updated_fields["name"] = new_name
            if new_number:
                updated_fields["number"] = new_number
            if new_desc:
                updated_fields["description"] = new_desc
            if updated_fields:
                db_crud.update_by_id("vlans", vlan_id, **updated_fields)
                print(f"✅ VLAN {current[1]} actualizada correctamente.")
            else:
                print("⚠️ No se realizaron cambios.")
        elif choice == "3":
            # Selecciona la VLAN a eliminar
            if not vlans:
                print("⚠️ No hay VLANs para eliminar.")
                continue
            vlan_idx = select_from_list([v[1] for v in vlans], "Selecciona VLAN a eliminar:")
            if vlan_idx is None:
                continue
            vlan_id = vlans[vlan_idx][0]
            db_crud.delete_by_id("vlans", vlan_id)
            print(f"✅ VLAN {vlans[vlan_idx][1]} eliminada correctamente.")
        elif choice == "4":
            # Asignar VLAN a dispositivo
            devices = db_manager.list_devices()
            if not devices:
                print("⚠️ No hay dispositivos disponibles.")
                continue
            dev_idx = select_from_list([d[1] for d in devices], "Selecciona dispositivo:")
            if dev_idx is None:
                continue
            device_id = devices[dev_idx][0]

            if not vlans:
                print("⚠️ No hay VLANs para asignar.")
                continue
            vlan_idx = select_from_list([v[1] for v in vlans], "Selecciona VLAN:")
            if vlan_idx is None:
                continue
            vlan_id = vlans[vlan_idx][0]

            iface = input("Interfaces (separadas por coma, opcional): ").strip()
            db_manager.assign_vlan_to_device(device_id, vlan_id, iface)
            print(f"✅ VLAN asignada correctamente al dispositivo.")
        else:
            print("❌ Opción inválida.")



# ---------------------------
# CRUD Protocolos y asignación
# ---------------------------
def manage_protocols():
    while True:
        protocols = db_manager.list_protocols()
        print("\n=== Protocolos ===")
        if protocols:
            table = [["#", "Name", "Description"]]
            for idx, p in enumerate(protocols, 1):
                table.append([idx, p[1], p[2]])
            print(tabulate(table, headers="firstrow", tablefmt="grid"))
        else:
            print("⚠️ No hay protocolos registrados.")
        print("\nOpciones:")
        print("1. Agregar Protocolo")
        print("2. Asignar Protocolo a dispositivo")
        print("0. Volver")
        choice = input("Selecciona una opción: ").strip()
        if choice == "0":
            break
        elif choice == "1":
            name = input("Nombre Protocolo: ")
            desc = input("Descripción: ")
            db_manager.add_protocol(name, desc)
            print(f"✅ Protocolo {name} agregado correctamente.")
        elif choice == "2":
            devices = db_manager.list_devices()
            dev_idx = select_from_list([d[1] for d in devices], "Selecciona dispositivo:")
            if dev_idx is None:
                continue
            device_id = devices[dev_idx][0]
            proto_idx = select_from_list([p[1] for p in protocols], "Selecciona protocolo:")
            if proto_idx is None:
                continue
            protocol_id = protocols[proto_idx][0]
            config = input("Configuración opcional: ").strip()
            db_manager.assign_protocol_to_device(device_id, protocol_id, config)
            print(f"✅ Protocolo asignado correctamente al dispositivo.")
        else:
            print("❌ Opción inválida.")

# ---------------------------
# CRUD Rutas estáticas
# ---------------------------
def manage_routes(device_id):
    while True:
        routes = db_manager.list_routes(device_id)
        print("\n=== Rutas estáticas ===")
        if routes:
            table = [["#", "Destino", "Máscara", "Next Hop", "Protocolo"]]
            for idx, r in enumerate(routes, 1):
                table.append([idx, r[2], r[3], r[4], r[5]])
            print(tabulate(table, headers="firstrow", tablefmt="grid"))
        else:
            print("⚠️ No hay rutas registradas.")
        print("\nOpciones:")
        print("1. Agregar Ruta")
        print("0. Volver")
        choice = input("Selecciona una opción: ").strip()
        if choice == "0":
            break
        elif choice == "1":
            dest = input("Destino: ")
            mask = input("Máscara: ")
            nh = input("Next Hop: ")
            proto = input("Protocolo (opc): ")
            db_manager.add_route(device_id, dest, mask, nh, proto)
            print("✅ Ruta agregada correctamente.")
        else:
            print("❌ Opción inválida.")

# ---------------------------
# CRUD Enlaces físicos
# ---------------------------
def manage_links():
    while True:
        links = db_manager.list_links()
        print("\n=== Enlaces físicos ===")
        if links:
            table = [["#", "Interface A", "Interface B", "Descripción"]]
            for idx, l in enumerate(links, 1):
                table.append([idx, l[1], l[2], l[3]])
            print(tabulate(table, headers="firstrow", tablefmt="grid"))
        else:
            print("⚠️ No hay enlaces registrados.")
        print("\nOpciones:")
        print("1. Agregar Enlace")
        print("0. Volver")
        choice = input("Selecciona una opción: ").strip()
        if choice == "0":
            break
        elif choice == "1":
            interfaces = db_manager.list_all_interfaces()
            if not interfaces:
                print("⚠️ No hay interfaces disponibles para enlazar.")
                continue
            iface_a_idx = select_from_list([f"{i[1]}:{i[2]}" for i in interfaces], "Selecciona Interface A:")
            iface_b_idx = select_from_list([f"{i[1]}:{i[2]}" for i in interfaces], "Selecciona Interface B:")
            if iface_a_idx is None or iface_b_idx is None:
                continue
            desc = input("Descripción (opc): ")
            db_manager.add_link(interfaces[iface_a_idx][0], interfaces[iface_b_idx][0], desc)
            print("✅ Enlace agregado correctamente.")
        else:
            print("❌ Opción inválida.")

# ---------------------------
# CRUD Atributos extra
# ---------------------------
def manage_extra_attributes(device_id):
    while True:
        attrs = db_manager.list_extra_attributes(device_id)
        print("\n=== Atributos extra ===")
        if attrs:
            table = [["#", "Nombre", "Valor"]]
            for idx, a in enumerate(attrs, 1):
                table.append([idx, a[2], a[3]])
            print(tabulate(table, headers="firstrow", tablefmt="grid"))
        else:
            print("⚠️ No hay atributos extra.")
        print("\nOpciones:")
        print("1. Agregar Atributo")
        print("0. Volver")
        choice = input("Selecciona una opción: ").strip()
        if choice == "0":
            break
        elif choice == "1":
            name = input("Nombre atributo: ")
            value = input("Valor: ")
            db_manager.add_extra_attribute(device_id, name, value)
            print("✅ Atributo agregado correctamente.")
        else:
            print("❌ Opción inválida.")






# ---------------------------
# Menú principal
# ---------------------------
def manage_inventory_menu():
    while True:
        print("\n=== 📂 Cisco Inventory Manager ===")
        print("1. Gestionar Dispositivos")
        print("2. Gestionar VLANs")
        print("3. Gestionar Protocolos")
        print("4. Gestionar Enlaces físicos")
        print("0. Salir")
        choice = input("Selecciona una opción: ").strip()
        if choice == "1":
            while True:
                print("\n--- Dispositivos ---")
                print("1. Agregar dispositivo")
                print("2. Actualizar dispositivo")
                print("3. Eliminar dispositivo")
                print("4. Listar dispositivos")
                print("5. Gestionar Interfaces")
                print("6. Gestionar Rutas")
                print("7. Gestionar Atributos extra")
                print("0. Volver")
                sub_choice = input("Selecciona una opción: ").strip()
                devices = db_manager.list_devices()
                if sub_choice == "1":
                    add_device()
                elif sub_choice == "2":
                    update_device()
                elif sub_choice == "3":
                    delete_device()
                elif sub_choice == "4":
                    list_devices()
                elif sub_choice == "5":
                    sel_idx = select_from_list([d[1] for d in devices], "Selecciona dispositivo para interfaces:")
                    if sel_idx is not None:
                        manage_interfaces(devices[sel_idx][0])
                elif sub_choice == "6":
                    sel_idx = select_from_list([d[1] for d in devices], "Selecciona dispositivo para rutas:")
                    if sel_idx is not None:
                        manage_routes(devices[sel_idx][0])
                elif sub_choice == "7":
                    sel_idx = select_from_list([d[1] for d in devices], "Selecciona dispositivo para atributos extra:")
                    if sel_idx is not None:
                        manage_extra_attributes(devices[sel_idx][0])
                elif sub_choice == "0":
                    break
                else:
                    print("❌ Opción inválida.")
        elif choice == "2":
            manage_vlans()
        elif choice == "3":
            manage_protocols()
        elif choice == "4":
            manage_links()
        elif choice == "0":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida.")

# ---------------------------
# Ejecutar módulo directamente
# ---------------------------
if __name__ == "__main__":
    manage_inventory_menu()
