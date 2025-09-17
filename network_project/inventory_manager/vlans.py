# network_project/inventory_manager/vlans.py
from tabulate import tabulate
from database_manager import db_crud

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

def manage_vlans():
    while True:
        vlans = db_crud.list_all("vlans")
        print("\n=== VLANs ===")
        if vlans:
            table = [["#", "Name", "Number", "Description"]]
            for idx, v in enumerate(vlans, 1):
                table.append([idx, v[1], v[2], v[3]])
            print(tabulate(table, headers="firstrow", tablefmt="grid"))
        else:
            print("⚠️ No hay VLANs registradas.")

        print("\nOpciones:")
        print("1. Agregar VLAN")
        print("2. Editar VLAN")
        print("3. Eliminar VLAN")
        print("0. Volver")
        choice = input("Selecciona una opción: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            name = input("Nombre VLAN: ").strip()
            number = input("Número VLAN: ").strip()
            desc = input("Descripción: ").strip()
            db_crud.insert("vlans", name=name, number=number, description=desc)
            print(f"✅ VLAN {name} agregada correctamente.")
        elif choice == "2":
            if not vlans:
                print("⚠️ No hay VLANs para editar.")
                continue
            idx = select_from_list([v[1] for v in vlans], "Selecciona VLAN a editar:")
            if idx is None:
                continue
            vlan = vlans[idx]
            vlan_id = vlan[0]
            new_name = input(f"Nombre [{vlan[1]}]: ").strip()
            new_number = input(f"Número [{vlan[2]}]: ").strip()
            new_desc = input(f"Descripción [{vlan[3]}]: ").strip()
            updated_fields = {}
            if new_name: updated_fields["name"] = new_name
            if new_number: updated_fields["number"] = new_number
            if new_desc: updated_fields["description"] = new_desc
            if updated_fields:
                db_crud.update_by_id("vlans", vlan_id, **updated_fields)
                print(f"✅ VLAN {vlan[1]} actualizada correctamente.")
            else:
                print("⚠️ No se realizaron cambios.")
        elif choice == "3":
            if not vlans:
                print("⚠️ No hay VLANs para eliminar.")
                continue
            idx = select_from_list([v[1] for v in vlans], "Selecciona VLAN a eliminar:")
            if idx is None:
                continue
            vlan_id = vlans[idx][0]
            db_crud.delete_by_id("vlans", vlan_id)
            print(f"✅ VLAN {vlans[idx][1]} eliminada correctamente.")
        else:
            print("❌ Opción inválida.")
