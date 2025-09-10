# main_telnet.py (modificado)
import os
import re
from netmiko import ConnectHandler
# Importar el módulo de escaneo
from network_scanner import scan_and_update

# Diccionario con los archivos de configuración
config_files = {
    "1": {"name": "Bastion", "file": "Configuracion_Bastion.txt"},
    "2": {"name": "Routers", "file": "Configuracion_Routers.txt"},
    "3": {"name": "Switches", "file": "Configuracion_Switches.txt"}
}


def mostrar_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Configurar Bastion")
    print("2. Configurar Routers")
    print("3. Configurar Switches")
    print("4. Escanear red y actualizar base de datos")
    print("5. Salir")
    return input("\nSelecciona una opción: ").strip()


# ... (el resto del código permanece igual hasta la función main)

def main():
    while True:
        opcion = mostrar_menu()

        if opcion in ["1", "2", "3"]:
            print("\n1. Ver configuración")
            print("2. Ejecutar configuración en el dispositivo")
            sub_opcion = input("\nSelecciona una opción: ").strip()

            if sub_opcion == "1":
                mostrar_configuracion(opcion)
            elif sub_opcion == "2":
                ejecutar_configuracion(opcion)
            else:
                print("\n❌ Opción inválida.")

        elif opcion == "4":
            # Nueva opción: Escanear red
            print("\n=== ESCANEO DE RED ===")
            network = input(
                "Introduce la red a escanear (ej: 192.168.0.0/24) o presiona Enter para usar la predeterminada: ").strip()
            if network:
                scan_and_update(network)
            else:
                scan_and_update()

        elif opcion == "5":
            print("\n👋 Saliendo del programa...")
            break

        else:
            print("\n❌ Opción inválida.")


if __name__ == "__main__":
    main()