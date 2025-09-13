# modules/bastion_router/main_bastion_router.py

from .sync_bastion_db import sync_bastion
from .connect_bastion import connect_to_bastion

def show_interfaces():
    interfaces = connect_to_bastion()
    if not interfaces:
        print("❌ No se pudieron obtener interfaces.")
        return

    print("\n=== Bastion Interfaces ===")
    for intf in interfaces:
        print(f"- {intf['name']}: IP={intf['ip']}, MAC={intf['mac']}, STATUS={intf['status']}")

def bastion_menu():
    while True:
        print("\n=== Bastion Management Menu ===")
        print("1️⃣  Sync Bastion DB")
        print("2️⃣  Show Interfaces")
        print("0️⃣  Return to Main Menu")

        choice = input("Select an option: ")

        if choice == "1":
            sync_bastion()
        elif choice == "2":
            show_interfaces()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

# Función main exportable para el menú principal
def main():
    bastion_menu()

if __name__ == "__main__":
    main()
