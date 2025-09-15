# network_monitor/main.py

def main_menu():
    """Menú principal para seleccionar acción"""
    while True:
        devices = get_all_devices()
        print("\n📋 Network Monitor - Menú Principal")
        if not devices:
            print("No hay dispositivos registrados. Debes agregar uno primero.")
            add_new_device()
            continue

        print("\nDispositivos existentes:")
        for idx, dev in enumerate(devices, start=1):
            print(f"{idx}. {dev[1]} | IP: {dev[2]}")  # dev = (id, hostname, ip, mac)

        print(f"{len(devices)+1}. Agregar nuevo dispositivo")
        print(f"{len(devices)+2}. Borrar base de datos (reset DB)")
        print("0. Salir")

        choice = input("Seleccione una opción: ").strip()
        if choice == "0":
            print("👋 Saliendo...")
            break
        elif choice == str(len(devices)+1):
            add_new_device()
        elif choice == str(len(devices)+2):
            from modules.db_manager.reset_db import reset_database
            reset_database()
        elif choice.isdigit() and 1 <= int(choice) <= len(devices):
            selected_device = devices[int(choice)-1]
            manage_device(selected_device)
        else:
            print("Opción inválida, intente nuevamente.")
