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
        device_info = register_device()
    else:
        device_info = devices_in_db[0]
        print(f"🔹 Se encontró dispositivo registrado: {device_info['hostname']} ({device_info['ip']})")

    ssh_output = ssh_main(device_info)
    parsed_data = genie_main(ssh_output)
    db_main(device_info, parsed_data)
    save_json_output(device_info, parsed_data)
    table_main(parsed_data)

if __name__ == "__main__":
    main()
