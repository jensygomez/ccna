# modules/bastion_scanner.py (versión simplificada)
import subprocess
import telnetlib
from .utils import validar_ip


def escanear_bastion_manual():
    """Permite ingresar manualmente la IP del Bastion y sus credenciales"""
    print("\n🎯 CONEXIÓN AL BASTION")
    print("=" * 40)

    # Pedir IP del Bastion
    while True:
        ip_manual = input("Ingresa la IP del Bastion [192.168.18.110]: ").strip()
        if not ip_manual:
            ip_manual = "192.168.18.110"

        if validar_ip(ip_manual):
            # Verificar si responde al ping
            try:
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip_manual],
                                        capture_output=True, text=True)

                if result.returncode == 0:
                    print(f"✅ {ip_manual} responde al ping")
                    break
                else:
                    print("❌ La IP no responde al ping. Verifica la conexión.")
                    continue
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        else:
            print("❌ IP inválida")
            continue

    # Pedir credenciales
    username = input("Usuario del Bastion [bastion]: ").strip() or "bastion"
    password = input("Password del Bastion [bastion]: ").strip() or "bastion"

    return [{
        "ip": ip_manual,
        "username": username,
        "password": password
    }]


def conectar_bastion(ip, username="bastion", password="bastion"):
    """Intenta conectar al Bastion y devuelve la conexión Telnet"""
    try:
        print(f"🔄 Conectando a {ip} con {username}/{password}...")
        tn = telnetlib.Telnet(ip, timeout=10)

        # Leer prompt de login
        login_output = tn.read_until(b"Username:", timeout=5)
        if b"Username:" not in login_output:
            login_output = tn.read_until(b"login:", timeout=5)

        # Enviar username
        tn.write(username.encode() + b"\n")

        # Leer prompt de password
        password_output = tn.read_until(b"Password:", timeout=5)
        tn.write(password.encode() + b"\n")

        # Esperar prompt de comando
        output = tn.read_until(b"#", timeout=5).decode()

        if "#" in output or ">" in output:
            print(f"✅ Conexión exitosa a {ip}")
            return tn
        else:
            print("❌ No se pudo obtener prompt de comando. Verifica las credenciales.")
            print("💡 Output recibido:", output[:100] + "..." if len(output) > 100 else output)
            return None

    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None