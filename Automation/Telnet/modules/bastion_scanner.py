# modules/bastion_scanner.py
from .network_discovery import descubrir_redes_locales


def seleccionar_ip_red(redes_detectadas):
    """Permite seleccionar una IP de la red detectada"""
    print("\n🎯 SELECCIONA UNA RED PARA EL BASTION")
    print("=" * 40)

    # Mostrar opciones de redes
    for i, red in enumerate(redes_detectadas, 1):
        print(f"{i}. Red: {red['red']}/24 - Interfaz: {red['interface']}")

    print(f"{len(redes_detectadas) + 1}. Ingresar IP manualmente")
    print(f"{len(redes_detectadas) + 2}. Usar IP por defecto (192.168.18.110)")

    # Solicitar selección
    while True:
        try:
            opcion = input(f"\nSelecciona una opción [1-{len(redes_detectadas) + 2}]: ").strip()

            if not opcion:
                return "192.168.18.110"  # Default

            opcion = int(opcion)

            if 1 <= opcion <= len(redes_detectadas):
                red_seleccionada = redes_detectadas[opcion - 1]
                ip_base = red_seleccionada['red'][:-1]  # Remover el último 0
                return f"{ip_base}110"  # Ejemplo: 192.168.18.110

            elif opcion == len(redes_detectadas) + 1:
                return input("Ingresa la IP manualmente: ").strip() or "192.168.18.110"

            elif opcion == len(redes_detectadas) + 2:
                return "192.168.18.110"

            else:
                print("❌ Opción inválida. Intenta nuevamente.")

        except ValueError:
            print("❌ Por favor ingresa un número válido.")
        except Exception as e:
            print(f"❌ Error: {e}")
            return "192.168.18.110"


def escanear_bastion_manual():
    """Escanea y configura conexión al bastion de forma manual con selección de red"""
    print("\n🎯 CONEXIÓN AL BASTION")
    print("=" * 40)

    # Obtener redes detectadas
    redes = descubrir_redes_locales()

    # Seleccionar IP automáticamente
    ip_bastion = seleccionar_ip_red(redes)

    # Configuración de credenciales
    username = input("Ingresa el username [cisco]: ").strip() or "cisco"
    password = input("Ingresa el password [cisco123]: ").strip() or "cisco123"

    print(f"\n✅ Configuración del Bastion:")
    print(f"   IP: {ip_bastion}")
    print(f"   Username: {username}")
    print(f"   Password: {password}")

    return [{
        'ip': ip_bastion,
        'username': username,
        'password': password,
        'protocol': 'telnet'
    }]


# Las otras funciones (conectar_bastion, etc.) se mantienen igual
def conectar_bastion(host, username, password, port=23):
    """Conecta al dispositivo via Telnet"""
    import telnetlib
    import time

    try:
        print(f"🔗 Conectando a {host}...")
        tn = telnetlib.Telnet(host, port, timeout=10)

        # Login process
        tn.read_until(b"Username: ", timeout=5)
        tn.write(username.encode('ascii') + b"\n")

        tn.read_until(b"Password: ", timeout=5)
        tn.write(password.encode('ascii') + b"\n")

        time.sleep(1)

        # Verificar conexión exitosa
        output = tn.read_very_eager().decode('ascii')
        if "Login invalid" in output or "Failed" in output:
            print("❌ Error de autenticación")
            return None

        print("✅ Conexión exitosa al Bastion!")
        return tn

    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None