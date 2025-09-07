"""
Módulo para las operaciones del menú"""

import os
from modules import switch_info

def clear_screen():
    """Limpia la pantalla de la terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu():
    """Menú principal"""
    while True:
        print("\n📋 MENÚ PRINCIPAL")
        print("1. Obtener información del switch")
        print("2. Salir")
        
        opcion = input("\nSelecciona una opción (1-2): ")
        
        if opcion == "1":
            switch_info.test_connection_menu() 
        elif opcion == "2":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

def press_enter_to_continue():
    """Pausa hasta que se presione Enter"""
    input("\n⏎ Presiona Enter para continuar...")
