# NetMonDB/main_NetMonDB.py


# NetMonDB/main_NetMonDB.py
# main_NetMonDB.py
from core.db_manager.main_db_manager import db_main, check_devices_in_db
from core.utils.main_utils import register_device
from core.ssh_connector.main_ssh_connector import ssh_main
from core.genie_parser.main_genie_parser import genie_main
from core.table_display.main_table_display import table_main

def main():
    print("🚀 Iniciando NetMonDB...")

    devices_in_db = check_devices_in_db()

    if not devices_in_db:
        # Registrar primer dispositivo
        device_info = register_device()
        print("📌 Dispositivo registrado. Vuelve al menú principal una vez pegada la configuración en el dispositivo.")
        return

    # Tomamos el primer dispositivo de la DB
    device_info = devices_in_db[0]
    print(f"\n🔹 Dispositivo encontrado en DB: {device_info['hostname']} ({device_info['ip']})")

    # 1️⃣ SSH + parseo + guardar JSON en outputs/
    raw_output = ssh_main(device_info)
    parsed_data = genie_main(raw_output)

    # 2️⃣ Guardar en DB
    db_main(device_info, parsed_data)

    # 3️⃣ Mostrar tabla
    table_main()

if __name__ == "__main__":
    main()
