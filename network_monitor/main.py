#network_monitor/main.py
from modules.db_manager.database import init_db
from modules.credentials_manager.creds import request_credentials
from modules.ssh_manager.ssh_handler import connect_and_run

def main():
    print("🚀 Iniciando Network Monitor...\n")

    # Inicializar DB (si no existe aún)
    init_db()

    # Solicitar IP del bastión
    ip = input("Ingrese la IP del bastión: ").strip()

    # Obtener credenciales (de DB o pidiéndolas al usuario)
    username, password = request_credentials(ip)

    # Conectar vía SSH y ejecutar comando
    try:
        output = connect_and_run(ip, username, password, command="show version")
        print("\n📄 Información del dispositivo:\n")
        print(output)

    except RuntimeError as err:
        print(f"❌ {err}")

if __name__ == "__main__":
    main()
