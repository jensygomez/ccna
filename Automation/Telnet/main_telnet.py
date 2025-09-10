# main_telnet.py
import os
import re
import telnetlib
import time
import getpass
import csv
from datetime import datetime

# Importar el módulo de escaneo mejorado
from network_scanner import scan_and_update, mostrar_resumen_escaneo

# Diccionario con los archivos de configuración
config_files = {
    "1": {"name": "Bastion", "file": "Configuracion_Bastion.txt"},
    "2": {"name": "Routers", "file": "Configuracion_Routers.txt"},
    "3": {"name": "Switches", "file": "Configuracion_Switches.txt"}
}


class CiscoTelnetClient:
    def __init__(self, host):
        self.host = host
        self.tn = None
        self.hostname = "Dispositivo"
        self.current_mode = "exec"

    def connect(self, username, password):
        """Conectar y hacer login"""
        print(f"🔄 Conectando a {self.host}...")
        try:
            self.tn = telnetlib.Telnet(self.host, timeout=10)

            # Esperar prompt de login
            login_output = self.tn.read_until(b"Username: ", timeout=5).decode()
            if "Username:" not in login_output:
                login_output = self.tn.read_until(b"login: ", timeout=5).decode()

            self.tn.write(username.encode() + b"\n")

            # Leer prompt de password
            password_output = self.tn.read_until(b"Password: ", timeout=5).decode()
            self.tn.write(password.encode() + b"\n")

            # Esperar prompt de comando
            output = self.tn.read_until(b"#", timeout=10).decode()

            # Detectar hostname del prompt
            match = re.search(r'(\S+)[#>]', output)
            if match:
                self.hostname = match.group(1)

            print(f"✅ Login exitoso! Hostname: {self.hostname}")
            return True

        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False

    def send_config_commands(self, commands):
        """Enviar comandos de configuración"""
        try:
            # Entrar en modo configuración
            print("🚀 Entrando en modo configuración...")
            self.tn.write(b"configure terminal\n")
            time.sleep(1)

            # Enviar cada comando
            for cmd in commands:
                if cmd.strip() and not cmd.strip().startswith("!"):
                    print(f"📤 Enviando: {cmd}")
                    self.tn.write(cmd.encode() + b"\n")
                    time.sleep(0.5)  # Pequeña pausa entre comandos

            # Salir del modo configuración
            self.tn.write(b"end\n")
            time.sleep(1)

            # Guardar configuración
            print("💾 Guardando configuración...")
            self.tn.write(b"write memory\n")
            time.sleep(2)

            # Verificar que se guardó correctamente
            output = self.tn.read_very_eager().decode()
            if "Building configuration" in output or "[OK]" in output:
                print("✅ Configuración guardada correctamente")
            else:
                print("⚠️  Configuración enviada, pero verifique el guardado manualmente")

            return True

        except Exception as e:
            print(f"❌ Error enviando comandos: {e}")
            return False

    def close(self):
        """Cerrar conexión"""
        if self.tn:
            try:
                self.tn.write(b"exit\n")
                time.sleep(1)
                self.tn.close()
                print("🔌 Conexión cerrada")
            except:
                pass


def mostrar_menu():
    """Mostrar el menú principal"""
    print("\n" + "=" * 60)
    print("           🚀 MENU PRINCIPAL - TELNET MANAGER")
    print("=" * 60)
    print("1. 📋 Configurar Bastion")
    print("2. 🔄 Configurar Routers")
    print("3. 🔀 Configurar Switches")
    print("4. 🔍 Escanear red y actualizar base de datos")
    print("5. 📊 Ver base de datos de dispositivos")
    print("6. ❌ Salir")
    print("=" * 60)
    return input("\nSelecciona una opción: ").strip()


def validar_ip(ip):
    """Validar formato de dirección IP"""
    patron = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if re.match(patron, ip):
        octetos = ip.split(".")
        return all(0 <= int(octeto) <= 255 for octeto in octetos)
    return False


def mostrar_configuracion(opcion):
    """Mostrar el contenido del archivo de configuración"""
    archivo = config_files[opcion]["file"]
    nombre = config_files[opcion]["name"]

    if os.path.exists(archivo):
        print(f"\n" + "=" * 60)
        print(f"           📋 CONFIGURACIÓN {nombre.upper()}")
        print("=" * 60)
        with open(archivo, "r", encoding='utf-8') as f:
            contenido = f.read()
            print(contenido)
        print("=" * 60)
    else:
        print(f"\n❌ No se encontró el archivo {archivo}")


def seleccionar_dispositivo():
    """Permitir al usuario seleccionar un dispositivo de la base de datos"""
    db_file = "db/dispositivos.csv"

    if not os.path.exists(db_file):
        print("❌ No se encontró la base de datos de dispositivos")
        print("⚠️  Ejecuta primero el escaneo de red (Opción 4)")
        return None

    try:
        with open(db_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            dispositivos = list(reader)

        if not dispositivos:
            print("❌ No hay dispositivos en la base de datos")
            return None

        print("\n" + "=" * 60)
        print("           📋 DISPOSITIVOS DISPONIBLES")
        print("=" * 60)

        for i, dispositivo in enumerate(dispositivos, 1):
            emoji = "🔄" if dispositivo['Tipo'] == 'Router' else "🔀" if dispositivo['Tipo'] == 'Switch' else "🛡️" if \
            dispositivo['Tipo'] == 'Bastion' else "🖥️"
            print(f"{i:2d}. {emoji} {dispositivo['IP']:15} → {dispositivo['Hostname']:15} ({dispositivo['Tipo']})")

        print("=" * 60)
        seleccion = input("\nSelecciona un dispositivo (número) o ingresa una IP manualmente: ").strip()

        if seleccion.isdigit():
            idx = int(seleccion) - 1
            if 0 <= idx < len(dispositivos):
                return dispositivos[idx]['IP']
            else:
                print("❌ Selección inválida")
                return None
        else:
            if validar_ip(seleccion):
                return seleccion
            else:
                print("❌ IP inválida")
                return None

    except Exception as e:
        print(f"❌ Error leyendo la base de datos: {e}")
        return None


def ejecutar_configuracion(opcion):
    """Ejecutar configuración en un dispositivo"""
    dispositivo_nombre = config_files[opcion]["name"]
    archivo = config_files[opcion]["file"]

    # Verificar archivo de configuración
    if not os.path.exists(archivo):
        print(f"\n❌ No se encontró el archivo {archivo}")
        return

    print(f"\n" + "=" * 60)
    print(f"           ⚙️ CONFIGURANDO {dispositivo_nombre.upper()}")
    print("=" * 60)

    # Seleccionar dispositivo
    ip = seleccionar_dispositivo()
    if not ip:
        # Si no seleccionó de la BD, pedir IP manualmente
        ip = input("IP del dispositivo: ").strip()
        if not validar_ip(ip):
            print("\n❌ IP inválida.")
            return

    # Solicitar credenciales
    username = input("Usuario Telnet: ").strip()
    password = getpass.getpass("Contraseña Telnet: ").strip()

    # Leer comandos del archivo (ignorar comentarios y líneas vacías)
    with open(archivo, "r", encoding='utf-8') as f:
        comandos = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith("!")]

    # Conectar y configurar
    client = CiscoTelnetClient(ip)

    if client.connect(username, password):
        print("✅ Conexión establecida, enviando configuración...")
        if client.send_config_commands(comandos):
            print(f"✅ Configuración aplicada correctamente en {dispositivo_nombre}.")
        else:
            print(f"❌ Error aplicando configuración en {dispositivo_nombre}.")
    else:
        print(f"❌ No se pudo conectar al dispositivo {ip}")

    client.close()


def ver_base_datos():
    """Mostrar el contenido de la base de datos de dispositivos"""
    db_file = "db/dispositivos.csv"

    if not os.path.exists(db_file):
        print("❌ No se encontró la base de datos de dispositivos")
        print("⚠️  Ejecuta primero el escaneo de red (Opción 4)")
        return

    try:
        with open(db_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            dispositivos = list(reader)

        if not dispositivos:
            print("❌ No hay dispositivos en la base de datos")
            return

        print("\n" + "=" * 80)
        print("                           📊 BASE DE DATOS DE DISPOSITIVOS")
        print("=" * 80)
        print(f"{'#':<3} {'IP':<15} {'Hostname':<15} {'Tipo':<10} {'MAC':<20} {'Última Actualización'}")
        print("-" * 80)

        for i, dispositivo in enumerate(dispositivos, 1):
            emoji = "🔄" if dispositivo['Tipo'] == 'Router' else "🔀" if dispositivo['Tipo'] == 'Switch' else "🛡️" if \
            dispositivo['Tipo'] == 'Bastion' else "🖥️"
            print(
                f"{i:<3} {emoji} {dispositivo['IP']:<15} {dispositivo['Hostname']:<15} {dispositivo['Tipo']:<10} {dispositivo['MAC']:<20} {dispositivo['ÚltimaActualización']}")

        print("=" * 80)
        print(f"Total de dispositivos: {len(dispositivos)}")

    except Exception as e:
        print(f"❌ Error leyendo la base de datos: {e}")


def main():
    """Función principal"""
    print("🚀 Iniciando Telnet Manager...")

    # Verificar si existe la carpeta db
    if not os.path.exists("db"):
        os.makedirs("db")
        print("📁 Carpeta 'db' creada")

    while True:
        opcion = mostrar_menu()

        if opcion in ["1", "2", "3"]:
            print(f"\n📋 Has seleccionado: {config_files[opcion]['name']}")
            print("1. Ver configuración")
            print("2. Ejecutar configuración en dispositivo")
            sub_opcion = input("\nSelecciona una opción: ").strip()

            if sub_opcion == "1":
                mostrar_configuracion(opcion)
            elif sub_opcion == "2":
                ejecutar_configuracion(opcion)
            else:
                print("\n❌ Opción inválida.")

        elif opcion == "4":
            # Escanear red
            print("\n" + "=" * 60)
            print("           🔍 ESCANEO DE RED")
            print("=" * 60)
            network = input(
                "Introduce la red a escanear (ej: 192.168.0.0/24)\n o presiona Enter para usar la predeterminada: ").strip()

            if network:
                scan_and_update(network)
            else:
                scan_and_update()

            input("\nPresiona Enter para continuar...")

        elif opcion == "5":
            # Ver base de datos
            ver_base_datos()
            input("\nPresiona Enter para continuar...")

        elif opcion == "6":
            print("\n👋 Saliendo del programa...")
            print("¡Hasta pronto! 🚀")
            break

        else:
            print("\n❌ Opción inválida. Por favor, selecciona 1-6.")
            input("Presiona Enter para continuar...")


if __name__ == "__main__":
    main()