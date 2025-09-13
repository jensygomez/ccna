from modules.database_manager import main_database_manager

def main():
    while True:
        print("\n=== Netmiko Project Menu ===")
        print("1️⃣  Sync Bastion DB")
        print("2️⃣  Run Telnet Manager")
        print("3️⃣  Check Project")
        print("4️⃣  Verify Database")  # nueva opción
        print("0️⃣  Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            sync_bastion_db.main()
        elif choice == "2":
            main_telnet_manager.main()
        elif choice == "3":
            check_project.main()
        elif choice == "4":
            main_database_manager.main()  # llama al sub-menú
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")
