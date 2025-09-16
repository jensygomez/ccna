# NetMonDB/main_NetMonDB.py


# NetMonDB/main_NetMonDB.py
# NetMonDB/main_NetMonDB.py

from core.ssh_connector.main_ssh_connector import ssh_main
from core.genie_parser.main_genie_parser import genie_main
from core.db_manager.main_db_manager import db_main, check_devices_in_db
from core.table_display.main_table_display import table_main
from core.utils.main_utils import register_device, save_json_output

def main():
    print("🚀 Iniciando NetMonDB...")

    devices_in_db = check_devices_in_db()

    if not devices_in_db:
        # 1️⃣ Primer dispositivo: registro y configuración inicial
        device_info = register_device()

        # Guardar en DB inmediatamente (parsed_data=None ya que no hay SSH aún)
        db_main(device_info, parsed_data=None)

        print("\n📌 Dispositivo registrado y guardado en la base de datos.")
        print("Vuelve al menú principal una vez pegada la configuración en el dispositivo.")
        return  # Termina aquí hasta que SSH esté activo

    else:
        # 2️⃣ Dispositivo ya registrado: flujo completo
        device_info = devices_in_db[0]
        print(f"\n🔹 Dispositivo encontrado en DB: {device_info['hostname']} ({device_info['ip']})\n")

        # 🔌 Conexión SSH y obtención de show running-config
        try:
            ssh_output = ssh_main(device_info)
        except Exception as e:
            print(f"❌ Error al conectar vía SSH: {e}")
            return

        # 📄 Parseo con Genie
        parsed_data = genie_main(ssh_output)

        # 💾 Guardar/actualizar en DB y JSON
        db_main(device_info, parsed_data)
        save_json_output(device_info, parsed_data)

        # 📊 Mostrar en pantalla en tablas
        table_main(parsed_data)

if __name__ == "__main__":
    main()
