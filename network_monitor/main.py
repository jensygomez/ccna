# network_monitor/main.py


from modules.db_manager.database import (
    init_db, save_device_log, save_device_and_credentials,
    save_interfaces, show_device_summary
)
from modules.credentials_manager.creds import request_credentials
from modules.ssh_manager.ssh_handler import connect_and_run
from modules.parsers.interfaces import parse_interfaces
from modules.parsers.device_info import parse_hostname, parse_mac


def main():
    print("🚀 Iniciando Network Monitor...\n")

    # Inicializar DB
    init_db()

    # Solicitar IP
    ip = input("Ingrese la IP del bastión: ").strip()

    # Credenciales
    username, password = request_credentials(ip)

    try:
        # show version
        output = connect_and_run(ip, username, password, command="show version")
        print("\n📄 Información del dispositivo (show version):\n")
        print(output)

        # Parsear hostname y MAC
        hostname = parse_hostname(output)
        mac = parse_mac(output)

        # Guardar dispositivo + credenciales
        save_device_and_credentials(ip, hostname, mac, username, password)

        # Guardar log
        save_device_log(ip, "show version", output)
        print("💾 Log guardado en la base de datos.")

        # show ip interface brief
        interfaces_output = connect_and_run(ip, username, password, command="show ip interface brief")
        interfaces = parse_interfaces(interfaces_output)

        # Guardar interfaces
        save_interfaces(ip, interfaces)

        # Mostrar resumen
        show_device_summary(ip)

    except RuntimeError as err:
        print(f"❌ {err}")
    except Exception as ex:
        print(f"❌ Error inesperado: {ex}")


if __name__ == "__main__":
    main()
