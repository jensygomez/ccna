# modules/bastion_scanner.py
import subprocess
import telnetlib
from .utils import validar_ip


def escanear_bastion(network_cidr, timeout=1):
    """Escanea una red para encontrar dispositivos Cisco (Bastion)"""
    print(f"🔍 Buscando Bastion en {network_cidr}...")

    try:
        import ipaddress
        network = ipaddress.ip_network(network_cidr, strict=False)
        bastion_ips = []

        # Escanear solo los primeros 20 hosts para mayor velocidad
        hosts = list(network.hosts())[:20]

        for ip in hosts:
            ip_str = str(ip)
            try:
                # Ping rápido
                result = subprocess.run(['ping', '-c', '1', '-W', str(timeout), ip_str],
                                        capture_output=True, text=True)

                if result.returncode == 0:
                    # Verificar si responde a Telnet (posible Cisco)
                    if es_dispositivo_cisco(ip_str):
                        bastion_ips.append(ip_str)
                        print(f"✅ Bastion encontrado: {ip_str}")

            except:
                continue

        return bastion_ips

    except Exception as e:
        print(f"❌ Error escaneando red: {e}")
        return []


def es_dispositivo_cisco(ip, timeout=2):
    """Verifica si una IP es un dispositivo Cisco respondiendo a Telnet"""
    try:
        tn = telnetlib.Telnet(ip, timeout=timeout)
        tn.read_until(b"Username:", timeout=timeout)
        tn.write(b"cisco\n")
        tn.read_until(b"Password:", timeout=timeout)
        tn.write(b"cisco\n")
        output = tn.read_until(b"#", timeout=timeout).decode()
        tn.close()

        # Buscar indicadores de Cisco
        cisco_indicators = ["Bastion", "Router", "Switch", "cisco", "Cisco"]
        return any(indicator in output for indicator in cisco_indicators)

    except:
        return False


def conectar_bastion(ip, username="cisco", password="cisco"):
    """Intenta conectar al Bastion y devuelve la conexión Telnet"""
    try:
        print(f"🔄 Conectando a {ip}...")
        tn = telnetlib.Telnet(ip, timeout=10)

        # Login
        tn.read_until(b"Username:", timeout=5)
        tn.write(username.encode() + b"\n")
        tn.read_until(b"Password:", timeout=5)
        tn.write(password.encode() + b"\n")

        # Esperar prompt
        output = tn.read_until(b"#", timeout=5).decode()

        if "#" in output:
            print(f"✅ Conexión exitosa a {ip}")
            return tn
        else:
            print("❌ No se pudo obtener prompt de comando")
            return None

    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None