# network_project/inventory_manager/main_inventory_manager.py
from .devices import manage_devices
from .interfaces import manage_interfaces


def manage_inventory_menu():
    while True:
        print("\n=== 📦 Gestión de Inventario ===")
        print("1. Dispositivos")
        print("2. Interfaces")
        # print("3. VLANs")  <-- ya eliminado
        print("0. Volver")
        choice = input("Selecciona una opción: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            manage_devices()  # módulo devices.py
        elif choice == "2":
            manage_interfaces()  # módulo interfaces.py
        else:
            print("❌ Opción inválida.")

