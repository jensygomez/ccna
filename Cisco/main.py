#!/usr/bin/env python3
"""
MENÚ PRINCIPAL - Herramienta de Automatización Cisco
"""
import os
from modules import menu_operations

def clear_screen():
    """Limpia la pantalla de la terminal de forma confiable"""
    # Para Windows
    if os.name == 'nt':
        os.system('cls')
    # Para Unix/Linux/MacOS
    else:
        os.system('clear')




def main():
    """Función principal"""
    clear_screen()
    print("🔧 HERRAMIENTA DE AUTOMATIZACIÓN CISCO")
    print("======================================")
    
    # Mostrar menú principal
    menu_operations.main_menu()

if __name__ == "__main__":
    main()
