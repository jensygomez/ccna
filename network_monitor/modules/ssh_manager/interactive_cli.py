# network_monitor/modules/ssh_manager/interactive_cli.py

from netmiko import ConnectHandler
from modules.db_manager.database import get_credentials

def interactive_cli(device):
    ip = device[2]
    username, password = get_credentials(ip)

    device_params = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'password': password,
    }

    print(f"\n💻 Iniciando sesión interactiva con {device[1]} ({ip})")
    print("Escribe comandos como si estuvieras en la consola del dispositivo.")
    print("Para salir de la sesión, escribe '.exit'\n")

    try:
        # Abrir sesión SSH persistente
        with ConnectHandler(**device_params) as ssh_conn:
            while True:
                # Capturar prompt actual del dispositivo
                prompt = ssh_conn.find_prompt().strip()
                cmd = input(f"{prompt} ").strip()

                if cmd.lower() == ".exit":
                    print("🔒 Cerrando sesión interactiva.\n")
                    break
                if cmd == "":
                    continue

                output = ssh_conn.send_command(cmd)
                print(output)
    except Exception as e:
        print(f"❌ Error al conectar con {ip}: {e}")
