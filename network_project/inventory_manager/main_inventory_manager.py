# network_project/inventory_manager/main_inventory_manager.py
from . import devices
from . import vlans


def manage_inventory_menu():
    while True:
        print("\n=== 📂 Cisco Inventory Manager ===")
        print("1. Gestionar VLANs")
        print("2. Gestionar Dispositivos")
        print("0. Salir")
        choice = input("Selecciona una opción: ").strip()
        if choice == "1":
            from inventory_manager import vlans
            vlans.manage_vlans()
        elif choice == "2":
            devices.manage_devices()
        elif choice == "0":
            break
        else:
            print("❌ Opción inválida.")
