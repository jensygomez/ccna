import os
from exercises import ejercicio1_ip, ejercicio2_no_shutdown

def mostrar_menu():
    print("\n=== Entrenador CCNA CLI Modular ===")
    print("1. Ejercicio 1: Configurar IP en interfaz")
    print("2. Ejercicio 2: Levantar interfaz (no shutdown)")
    print("3. Salir")
    return input("Selecciona un ejercicio: ").strip()

def main():
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            ejercicio1_ip.ejecutar()
        elif opcion == "2":
            ejercicio2_no_shutdown.ejecutar()
        elif opcion == "3":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()
