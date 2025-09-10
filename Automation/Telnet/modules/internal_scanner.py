# modules/internal_scanner.py
import ipaddress


def escanear_red_desde_bastion(tn, red_interna="192.168.0.0/24"):
    """Escanea una red interna desde el Bastion via Telnet"""
    print(f"🔍 Escaneando red interna {red_interna} desde el Bastion...")

    try:
        network = ipaddress.ip_network(red_interna, strict=False)
        dispositivos_activos = []

        # Escanear solo una parte de la red para mayor velocidad
        hosts = list(network.hosts())[:50]  # Primeros 50 hosts

        for ip in hosts:
            ip_str = str(ip)

            # Ejecutar ping desde el Bastion
            tn.write(f"ping {ip_str} repeat 1 timeout 1\n".encode())
            output = tn.read_until(b"Success rate", timeout=2).decode()

            if "Success rate is 100 percent" in output or "Success rate is 0 percent" not in output:
                dispositivos_activos.append(ip_str)
                print(f"✅ {ip_str} - Activo")
            else:
                print(f"❌ {ip_str} - Inactivo")

            # Limpiar buffer
            tn.read_very_eager()

        return dispositivos_activos

    except Exception as e:
        print(f"❌ Error escaneando desde Bastion: {e}")
        return []