# network_project/inventory_manager/interfaces.py

from tabulate import tabulate
from database_manager import db_crud

def select_from_list(items, prompt="Selecciona un elemento:"):
    """Muestra una lista numerada y permite seleccionar un elemento."""
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


def manage_interfaces():
    while True:
        interfaces = db_crud.list_all("interfaces")
        print("\n=== 🌐 Interfaces ===")
        if interfaces:
            table = [["#", "Device ID", "Nombre", "Tipo (mode)", "IP", "Máscara", "Descripción", "Status"]]
            for idx, i in enumerate(interfaces, 1):
                # i[1]=device_id, i[2]=name, i[3]=mode, i[4]=ip, i[5]=status, i[6]=description
                table.append([
                    idx,          # #
                    i[1],         # Device ID
                    i[2],         # Nombre
                    i[3],         # Tipo (mode)
                    i[4],         # IP
                    i[5],         # Máscara (subnet_mask)
                    i[7],         # Descripción
                    i[6]          # Status
                    ])

            print(tabulate(table, headers="firstrow", tablefmt="grid"))
        else:
            print("⚠️ No hay interfaces registradas.")

        print("\nOpciones:")
        print("1. Agregar Interfaz")
        print("2. Editar Interfaz")
        print("3. Eliminar Interfaz")
        print("0. Volver")
        choice = input("Selecciona una opción: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            # Selección del dispositivo
            devices = db_crud.list_all("devices")
            if not devices:
                print("⚠️ No hay dispositivos registrados. Registra uno primero.")
                continue
            dev_idx = select_from_list([d[1] for d in devices], "Selecciona el dispositivo:")
            if dev_idx is None:
                continue
            device_id = devices[dev_idx][0]

            # Selección del tipo de interfaz
            print("\nTipos de Interfaces:")
            print("1. Interfaces Físicas (GigabitEthernet, FastEthernet, Serial)")
            print("2. VLAN (SVI)")
            print("3. Loopback")
            print("4. Tunnel")
            print("5. Port-Channel")
            print("6. Otro / Personalizado")
            t_choice = input("Selecciona el tipo: ").strip()
            tipos = {
                "1": "Physical",
                "2": "VLAN",
                "3": "Loopback",
                "4": "Tunnel",
                "5": "Port-Channel",
                "6": "Custom"
            }
            iface_type = tipos.get(t_choice, "Custom")

            # Datos de la interfaz
            name = input("Nombre de la interfaz (ej: GigabitEthernet0/0, Vlan10): ").strip()
            ip = input("Dirección IP (ENTER si no aplica): ").strip()
            mask = input("Máscara (ENTER si no aplica, opcional): ").strip()
            desc = input("Descripción: ").strip()
            status = input("Status (up/down, opcional): ").strip()

            db_crud.insert(
                "interfaces",
                device_id=device_id,
                name=name,
                mode=iface_type,
                ip=ip,
                subnet_mask=mask,
                status=status,
                description=desc
            )
            print(f"✅ Interfaz {name} agregada correctamente.")

        elif choice == "2":
            if not interfaces:
                print("⚠️ No hay interfaces para editar.")
                continue
            idx = select_from_list([i[2] for i in interfaces], "Selecciona la interfaz a editar:")
            if idx is None:
                continue
            iface = interfaces[idx]
            iface_id = iface[0]

            new_name = input(f"Nombre [{iface[2]}]: ").strip()
            new_type = input(f"Tipo [{iface[3]}]: ").strip()
            new_ip = input(f"IP [{iface[4]}]: ").strip()
            new_mask = input(f"Máscara [{iface[7] if len(iface) > 7 else ''}]: ").strip()
            new_status = input(f"Status [{iface[5]}]: ").strip()
            new_desc = input(f"Descripción [{iface[6]}]: ").strip()

            updated_fields = {}
            if new_name: updated_fields["name"] = new_name
            if new_type: updated_fields["mode"] = new_type
            if new_ip: updated_fields["ip"] = new_ip
            if new_mask: updated_fields["subnet_mask"] = new_mask
            if new_status: updated_fields["status"] = new_status
            if new_desc: updated_fields["description"] = new_desc
            

            if updated_fields:
                db_crud.update_by_id("interfaces", iface_id, **updated_fields)
                print(f"✅ Interfaz {iface[2]} actualizada correctamente.")
            else:
                print("⚠️ No se realizaron cambios.")

        elif choice == "3":
            if not interfaces:
                print("⚠️ No hay interfaces para eliminar.")
                continue
            idx = select_from_list([i[2] for i in interfaces], "Selecciona la interfaz a eliminar:")
            if idx is None:
                continue
            iface_id = interfaces[idx][0]
            db_crud.delete_by_id("interfaces", iface_id)
            print(f"✅ Interfaz {interfaces[idx][2]} eliminada correctamente.")

        else:
            print("❌ Opción inválida.")
