import os
import re
from netmiko import ConnectHandler

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
    print("4. Salir")
    return input("\nSelecciona una opción: ").strip()

def validar_ip(ip):
    patron = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(patron, ip) and all(0 <= int(octeto) <= 255 for octeto in ip.split("."))

def mostrar_configuracion(opcion):
    archivo = config_files[opcion]["file"]
    if os.path.exists(archivo):
        print(f"\n=== CONTENIDO DE {archivo} ===\n")
        with open(archivo, "r") as f:
            print(f.read())
    else:
        print(f"\n❌ No se encontró el archivo {archivo}")

def ejecutar_configuracion(opcion):
    dispositivo_nombre = config_files[opcion]["name"]
    archivo = config_files[opcion]["file"]

    # Verificar archivo
    if not os.path.exists(archivo):
        print(f"\n❌ No se encontró el archivo {archivo}")
        return

    print(f"\n=== CONFIGURANDO {dispositivo_nombre.upper()} ===")

    # Solicitar datos de conexión
    ip = input("IP del dispositivo: ").strip()
    if not validar_ip(ip):
        print("\n❌ IP inválida.")
        return

    username = input("Usuario SSH: ").strip()
    password = input("Contraseña SSH: ").strip()

    dispositivo = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
    }

    try:
        print(f"\n🔗 Conectando a {ip} ({dispositivo_nombre})...")
        conexion = ConnectHandler(**dispositivo)

        # Leer comandos, ignorando comentarios
        with open(archivo, "r") as f:
            comandos = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith("!")]

        print(f"🚀 Enviando configuración desde {archivo}...")
        output = conexion.send_config_set(comandos)

        print("\n=== SALIDA DEL DISPOSITIVO ===\n")
        print(output)

        # Guardar cambios
        conexion.save_config()
        conexion.disconnect()
        print(f"\n✅ Configuración aplicada correctamente en {dispositivo_nombre}.")

    except Exception as e:
        print(f"\n❌ Error al configurar {dispositivo_nombre}: {e}")

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
            print("\n👋 Saliendo del programa...")
            break
        else:
            print("\n❌ Opción inválida.")

if __name__ == "__main__":
    main()
