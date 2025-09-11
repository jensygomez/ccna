# modules/internal_scanner.py
import ipaddress
from modules.database_manager import obtener_redes_de_db

from .utils import leer_base_datos, obtener_dispositivos_por_red


def mostrar_y_seleccionar_red():
    """Muestra las redes disponibles de la BD y permite seleccionar una"""
    dispositivos = leer_base_datos()

    if not dispositivos:
        print("❌ No hay dispositivos en la base de datos.")
        print("💡 Ejecuta primero un escaneo de red o usa valores por defecto")
        return "192.168.0.0/24"  # Valor por defecto

    redes = obtener_redes_de_db()

    if not redes:
        print("❌ No se pudieron extraer redes de la base de datos")
        return "192.168.0.0/24"

    print("\n📊 REDES DISPONIBLES EN BASE DE DATOS:")
    print("=" * 50)

    for i, red in enumerate(redes, 1):
        dispositivos_red = obtener_dispositivos_por_red(dispositivos, red)
        print(f"{i}. {red:15} ({len(dispositivos_red)} dispositivos)")

    print("=" * 50)

    try:
        seleccion = input("Selecciona una red (número) o Enter para default [1]: ").strip()
        if not seleccion:
            seleccion = "1"

        idx = int(seleccion) - 1
        if 0 <= idx < len(redes):
            red_seleccionada = redes[idx]
            print(f"✅ Red seleccionada: {red_seleccionada}")
            return red_seleccionada
        else:
            print("❌ Selección inválida, usando default")
            return "192.168.0.0/24"
    except ValueError:
        print("❌ Entrada inválida, usando default")
        return "192.168.0.0/24"


def escanear_red_desde_bastion(tn, red_interna="192.168.0.0/24"):
    """Escanea una red interna desde el Bastion usando la BD con doble verificación"""
    dispositivos = leer_base_datos()
    dispositivos_red = obtener_dispositivos_por_red(dispositivos, red_interna)

    if not dispositivos_red:
        print(f"❌ No hay dispositivos en la BD para la red {red_interna}")
        print("💡 Usando escaneo de rango completo...")
        return escanear_rango_completo(tn, red_interna)

    print(f"🔍 Escaneando {len(dispositivos_red)} dispositivos de la BD en {red_interna}...")

    dispositivos_activos = []

    for dispositivo in dispositivos_red:
        ip_str = dispositivo.get('IP', '')
        nombre = dispositivo.get('Hostname', 'Desconocido')
        tipo = dispositivo.get('Tipo', 'Desconocido')

        if not ip_str:
            continue

        try:
            # Primer ping
            tn.write(f"ping {ip_str} repeat 3 timeout 2\n".encode())
            output = tn.read_until(b"Success rate", timeout=3).decode()

            if "Success rate is 100 percent" in output:
                dispositivos_activos.append(ip_str)
                print(f"✅ {ip_str} - {nombre} ({tipo}) - Activo")
            elif "Success rate is 0 percent" in output:
                # Segundo ping para confirmar
                tn.write(f"ping {ip_str} repeat 2 timeout 1\n".encode())
                output2 = tn.read_until(b"Success rate", timeout=3).decode()
                if "Success rate is 0 percent" in output2:
                    print(f"❌ {ip_str} - {nombre} ({tipo}) - Inactivo")
                else:
                    dispositivos_activos.append(ip_str)
                    print(f"⚠️  {ip_str} - {nombre} ({tipo}) - Activo (con pérdidas)")
            else:
                dispositivos_activos.append(ip_str)
                print(f"⚠️  {ip_str} - {nombre} ({tipo}) - Activo (con pérdidas)")

            # Limpiar buffer
            try:
                tn.read_very_eager()
            except:
                pass

        except Exception as e:
            print(f"❌ Error escaneando {ip_str}: {e}")

    return dispositivos_activos



def escanear_rango_completo(tn, red_interna):
    """Escanea un rango completo como fallback"""
    print(f"🔍 Escaneo completo de {red_interna}...")

    try:
        network = ipaddress.ip_network(red_interna, strict=False)
        dispositivos_activos = []

        # Escanear solo los primeros 50 hosts para no demorar mucho
        hosts = list(network.hosts())[:50]

        for ip in hosts:
            ip_str = str(ip)

            try:
                tn.write(f"ping {ip_str} repeat 1 timeout 1\n".encode())
                output = tn.read_until(b"Success rate", timeout=2).decode()

                if "Success rate is 100 percent" in output:
                    dispositivos_activos.append(ip_str)
                    print(f"✅ {ip_str} - Activo")
                elif "Success rate is 0 percent" not in output:
                    dispositivos_activos.append(ip_str)
                    print(f"⚠️  {ip_str} - Activo (con pérdidas)")
                else:
                    print(f"❌ {ip_str} - Inactivo")

            except:
                continue

            # Limpiar buffer
            try:
                tn.read_very_eager()
            except:
                pass

        return dispositivos_activos

    except Exception as e:
        print(f"❌ Error en escaneo completo: {e}")
        return []