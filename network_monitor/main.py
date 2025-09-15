# network_monitor/main.py


# network_monitor/main.py

from modules.db_manager.init_device import add_new_device
from modules.db_manager.database import (
    init_db, get_all_devices, get_credentials,
    save_interfaces, show_device_summary
)
from modules.ssh_manager.ssh_handler import connect_and_run
from modules.parsers.interfaces import parse_interfaces
from modules.ssh_manager.interactive_cli import interactive_cli
from modules.db_manager.reset_db import reset_database


def configure_device(selected_device):
    """Conecta y actualiza información de un dispositivo existente"""
    ip = selected_device[2]
    creds = get_credentials(ip)
    if not creds:
        print(f"❌ No se encontraron credenciales para {ip}.")
        return
    username, password = creds

    try:
        # show version
        output = connect_and_run(ip, username, password, command="show version")
        print("\n📄 Información del dispositivo (show version):\n")
        print(output)

        # show ip interface brief
        interfaces_output = connect_and_run(ip, username, password, command="show ip interface brief")
        interfaces = parse_interfaces(interfaces_output)

        # Guardar interfaces
        save_interfaces(ip, interfaces)

        # Mostrar resumen
        show_device_summary(ip)

    except Exception as e:
        print(f"❌ Error al conectar con {ip}: {e}")


def main_menu():
    """Menú principal del Network Monitor"""
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
            reset_database()
        elif choice.isdigit() and 1 <= int(choice) <= len(devices):
            selected_device = devices[int(choice)-1]

            # Submenú de acciones sobre el dispositivo
            while True:
                print(f"\nDispositivo seleccionado: {selected_device[1]} | IP: {selected_device[2]}")
                print("1. Actualizar información del dispositivo")
                print("2. Abrir sesión interactiva (CLI)")
                print("0. Regresar al menú principal")
                sub_choice = input("Seleccione opción (0, 1 o 2): ").strip()

                if sub_choice == "1":
                    configure_device(selected_device)
                elif sub_choice == "2":
                    interactive_cli(selected_device)
                elif sub_choice == "0":
                    break
                else:
                    print("Opción inválida, intente nuevamente.")
        else:
            print("Opción inválida, intente nuevamente.")


def main():
    print("🚀 Iniciando Network Monitor...\n")
    init_db()  # Asegurarse de que la DB exista
    main_menu()


if __name__ == "__main__":
    main()
