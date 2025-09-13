# main_netmiko.py

# ------------------------------
# Imports de todos los módulos
# ------------------------------
from modules.bastion_router import main_bastion_router
from modules.telnet_manager import main_telnet_manager
from modules.database_manager import main_database_manager
import scripts.check_project as check_project

# ------------------------------
# Menú principal
# ------------------------------
def main_menu():
    while True:
        print("\n=== Netmiko Project Menu ===")
        print("1️⃣  Bastion Management")
        print("2️⃣  Run Telnet Manager")
        print("3️⃣  Check Project")
        print("4️⃣  Verify Database")
        print("0️⃣  Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            main_bastion_router.main()  # abre el menú del Bastion
        elif choice == "2":
            main_telnet_manager.main()  # Telnet Manager
        elif choice == "3":
            check_project.main()        # Check Project
        elif choice == "4":
            main_database_manager.main()  # Database Manager sub-menú
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

# ------------------------------
# Ejecutar main al correr el archivo
# ------------------------------
if __name__ == "__main__":
    main_menu()
