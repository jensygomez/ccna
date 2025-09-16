# network_project/main_network_project.py

# network_project/main_network_project.py

from inventory_manager.main_inventory_manager import manage_inventory_menu

def main():
    while True:
        print("\n=== 🚀 Network Project ===")
        print("1. Gestión de Dispositivos")
        print("0. Salir")
        choice = input("Selecciona una opción: ")
        if choice == "1":
            manage_inventory_menu()  # <--- llamar al menú correcto
        elif choice == "0":
            break
        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    main()
