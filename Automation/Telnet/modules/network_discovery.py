# modules/bastion_scanner.py (mejorado)
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

        # Escanear hosts relevantes (no todos para mayor velocidad)
        hosts = []
        for ip in network.hosts():
            # Escanear solo ciertos rangos comunes
            last_octet = int(str(ip).split('.')[-1])
            if last_octet in [1, 100, 110, 200, 254] or last_octet < 50:
                hosts.append(ip)
            if len(hosts) >= 30:  # Límite para no demorar mucho
                break

        for ip in hosts:
            ip_str = str(ip)
            try:
                # Ping rápido
                result = subprocess.run(['ping', '-c', '1', '-W', str(timeout), ip_str],
                                        capture_output=True, text=True)

                if result.returncode == 0:
                    print(f"📶 {ip_str} responde al ping, verificando si es Cisco...")
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


def escanear_bastion_manual():
    """Permite ingresar manualmente la IP del Bastion"""
    print("\n🎯 Escaneo manual del Bastion")
    print("=" * 40)

    while True:
        ip_manual = input("Ingresa la IP del Bastion (192.168.18.110): ").strip()

        if not ip_manual:
            ip_manual = "192.168.18.110"  # Valor por defecto

        if validar_ip(ip_manual):
            # Verificar si responde
            try:
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip_manual],
                                        capture_output=True, text=True)

                if result.returncode == 0:
                    if es_dispositivo_cisco(ip_manual):
                        return [ip_manual]
                    else:
                        print("❌ La IP responde pero no parece ser un dispositivo Cisco")
                        continue
                else:
                    print("❌ La IP no responde al ping")
                    continue

            except Exception as e:
                print(f"❌ Error verificando IP: {e}")
                continue
        else:
            print("❌ IP inválida")
            continue


def es_dispositivo_cisco(ip, timeout=2):
    """Verifica si una IP es un dispositivo Cisco respondiendo a Telnet"""
    try:
        print(f"   Probando Telnet en {ip}...")
        tn = telnetlib.Telnet(ip, timeout=timeout)

        # Leer prompt de login
        login_prompt = tn.read_until(b"Username:", timeout=timeout)
        if b"Username:" not in login_prompt:
            login_prompt = tn.read_until(b"login:", timeout=timeout)

        tn.write(b"cisco\n")
        tn.read_until(b"Password:", timeout=timeout)
        tn.write(b"cisco\n")

        output = tn.read_until(b"#", timeout=timeout).decode()
        tn.close()

        # Buscar indicadores de Cisco
        cisco_indicators = ["Bastion", "Router", "Switch", "cisco", "Cisco", ">", "#"]
        return any(indicator in output for indicator in cisco_indicators)

    except Exception as e:
        return False