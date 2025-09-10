# modules/internal_scanner.py (corregido)
import ipaddress


def escanear_red_desde_bastion(tn, red_interna="192.168.0.0/24"):
    """Escanea una red interna desde el Bastion via Telnet"""
    print(f"🔍 Escaneando red interna {red_interna} desde el Bastion...")

    try:
        network = ipaddress.ip_network(red_interna, strict=False)
        dispositivos_activos = []

        # Escanear solo hosts válidos (excluir network y broadcast)
        hosts = list(network.hosts())  # Esto excluye automáticamente network/broadcast

        # Limitar escaneo a un rango razonable
        hosts_a_escanear = hosts[:100]  # Primeros 100 hosts

        print(f"📊 Escaneando {len(hosts_a_escanear)} dispositivos...")

        for ip in hosts_a_escanear:
            ip_str = str(ip)

            # Ejecutar ping desde el Bastion
            tn.write(f"ping {ip_str} repeat 2 timeout 1\n".encode())
            output = tn.read_until(b"Success rate", timeout=3).decode()

            if "Success rate is 100 percent" in output or "Success rate is 50 percent" in output:
                dispositivos_activos.append(ip_str)
                print(f"✅ {ip_str} - Activo")
            elif "Success rate is 0 percent" not in output:
                # Si no es 0%, podría estar activo pero con pérdida de paquetes
                dispositivos_activos.append(ip_str)
                print(f"⚠️  {ip_str} - Posiblemente activo (con pérdidas)")
            else:
                print(f"❌ {ip_str} - Inactivo")

            # Limpiar buffer
            try:
                tn.read_very_eager()
            except:
                pass

        return dispositivos_activos

    except Exception as e:
        print(f"❌ Error escaneando desde Bastion: {e}")
        return []