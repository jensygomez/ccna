# NetMonDB/main_NetMonDB.py

from core.ssh_connector.main_ssh_connector import ssh_main
from core.genie_parser.main_genie_parser import genie_main
from core.db_manager.main_db_manager import db_main
from core.table_display.main_table_display import table_main

def main():
    print("🚀 Iniciando NetMonDB...")

    # 1️⃣ Conexión SSH y obtención de datos
    ssh_data = ssh_main()

    # 2️⃣ Parseo con Genie
    parsed_data = genie_main(ssh_data)

    # 3️⃣ Guardar/actualizar en DB
    db_main(parsed_data)

    # 4️⃣ Mostrar en tablas
    table_main(parsed_data)

if __name__ == "__main__":
    main()
