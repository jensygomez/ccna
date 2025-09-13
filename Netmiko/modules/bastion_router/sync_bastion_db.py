# modules/bastion_router/sync_bastion_db.py
from .connect_bastion import connect_to_bastion, get_lldp_neighbors
from modules.database_manager.db_utils import (
    init_db, add_or_update_device, add_or_update_interface, add_log, get_last_log_for_interface, add_or_update_lldp
)
import os
from netmiko import ConnectHandler

DB_PATH = os.path.join("modules", "database", "net_devices.db")


def sync_bastion():
    print("🔹 Sincronizando Bastion con DB...")

    # Inicializamos la DB
    init_db()

    # Aseguramos que Bastion esté en la tabla devices
    device_id = add_or_update_device(
        name="Bastion",
        type_="Router",
        ip="192.168.18.110",
        mac="N/A",
        model="ISR4331",
        location="Home Lab"
    )

    # Conectamos al Bastion y obtenemos interfaces
    try:
        bastion_conn = ConnectHandler(
            device_type="cisco_ios",
            host="192.168.18.110",
            username="bastion",
            password="bastion",
            secret="bastion"
        )
        bastion_conn.enable()
        print("✅ Conectado al Bastion")

        # Interfaces
        interfaces = connect_to_bastion()
        if interfaces:
            for intf in interfaces:
                name, ip, mac, status = intf["name"], intf["ip"], intf["mac"], intf["status"]

                add_or_update_interface(
                    device_id=device_id,
                    name=name,
                    mac=mac,
                    ip=ip,
                    status=status,
                    description=""
                )

                # Log si hubo cambio
                log_output = f"IP={ip}, MAC={mac}, STATUS={status}"
                last_log = get_last_log_for_interface(device_id, name)
                if last_log != log_output:
                    add_log(device_id, f"Sync {name}", log_output)

        # LLDP neighbors
        neighbors = get_lldp_neighbors(bastion_conn)
        for nbr in neighbors:
            add_or_update_lldp(
                device_id=device_id,
                local_intf=nbr.get("local_intf"),
                neighbor_name=nbr.get("neighbor_name"),
                neighbor_port=nbr.get("neighbor_port"),
                neighbor_ip=nbr.get("neighbor_ip"),
                neighbor_type=nbr.get("neighbor_type"),
                neighbor_model=nbr.get("neighbor_model"),
                timestamp=nbr.get("timestamp")
            )
        print(f"✅ LLDP neighbors synchronized ({len(neighbors)} found)")

        bastion_conn.disconnect()

    except Exception as e:
        print(f"❌ Error al conectar o sincronizar Bastion: {e}")

    print("✅ Sincronización completada.")


# ------------------------------
# Función main exportable para menú
# ------------------------------
def main():
    sync_bastion()


# ------------------------------
# Mantener ejecución directa
# ------------------------------
if __name__ == "__main__":
    main()
