# modules/database_manager/main_database_manager.py

from . import db_cleaner, db_viewer

def database_menu():
    while True:
        print("\n=== Database Manager Menu ===")
        print("1️⃣  Clean Database")
        print("2️⃣  View Database")
        print("0️⃣  Return to Main Menu")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            db_cleaner.main()  # Asegúrate que db_cleaner.py tenga una función main()
        elif choice == "2":
            db_viewer.main()   # Asegúrate que db_viewer.py tenga una función main()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

def main():
    database_menu()

# Mantener ejecución directa
if __name__ == "__main__":
    main()
