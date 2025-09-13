# modules/bastion_router/main_bastion_router.py
from .sync_bastion_db import sync_bastion
from .connect_bastion import connect_to_bastion, get_lldp_neighbors
from modules.database_manager.db_utils import init_db
from netmiko import ConnectHandler

def show_interfaces():
    """Mostrar interfaces del Bastion en pantalla"""
    interfaces = connect_to_bastion()
    if not interfaces:
        print("❌ No se pudieron obtener interfaces.")
        return

    print("\n=== Bastion Interfaces ===")
    for intf in interfaces:
        print(f"- {intf['name']}: IP={intf['ip']}, MAC={intf['mac']}, STATUS={intf['status']}")


def show_lldp_neighbors():
    """Mostrar LLDP neighbors del Bastion en pantalla"""
    try:
        conn = ConnectHandler(
            device_type="cisco_ios",
            host="192.168.18.110",
            username="bastion",
            password="bastion",
            secret="bastion"
        )
        conn.enable()
        neighbors = get_lldp_neighbors(conn)
        conn.disconnect()

        if not neighbors:
            print("❌ No LLDP neighbors found.")
            return

        print("\n=== Bastion LLDP Neighbors ===")
        for nbr in neighbors:
            print(f"- Local Intf: {nbr['local_intf']}, Neighbor: {nbr['neighbor_name']}, "
                  f"Port: {nbr['neighbor_port']}, IP: {nbr['neighbor_ip']}, Type: {nbr['neighbor_type']}")

    except Exception as e:
        print(f"❌ Error al obtener LLDP neighbors: {e}")


def main():
    """Menú Bastion Management"""
    while True:
        print("\n=== Bastion Management Menu ===")
        print("1️⃣  Sync Bastion DB")
        print("2️⃣  Show Interfaces")
        print("3️⃣  Show LLDP Neighbors")
        print("0️⃣  Return to Main Menu")

        choice = input("Select an option: ")

        if choice == "1":
            sync_bastion()
        elif choice == "2":
            show_interfaces()
        elif choice == "3":
            show_lldp_neighbors()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()

