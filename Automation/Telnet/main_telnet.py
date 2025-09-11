import sys

def mostrar_menu():
    print("\n=== Proyecto Telnet - Menú Principal ===")
    print("1. Telnet Manager (genérico)")
    print("2. Router Bastion")
    print("3. Core Switch")
    print("0. Salir")
    return input("Selecciona una opción: ")

def main():
    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            from modules.telnet_manager import main as telnet_main
            telnet_main.run()
        elif opcion == "2":
            from modules.bastion_router import main as bastion_main
            bastion_main.run()
        elif opcion == "3":
            from modules.core_switch import main as cs_main
            cs_main.run()
        elif opcion == "0":
            print("👋 Saliendo del sistema...")
            sys.exit(0)
        else:
            print("❌ Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    main()
