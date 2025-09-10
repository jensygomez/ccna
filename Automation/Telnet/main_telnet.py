# main_telnet.py (versión modular)
import os
import sys
from modules.network_discovery import descubrir_redes_locales, seleccionar_red
from modules.bastion_scanner import escanear_bastion, conectar_bastion
from modules.internal_scanner import escanear_red_desde_bastion


def escaneo_inteligente():
    """Flujo completo de escaneo inteligente"""
    print("🚀 INICIO DE ESCANEO INTELIGENTE")
    print("=" * 60)

    # 1. Descubrir redes locales
    interfaces = descubrir_redes_locales()
    if not interfaces:
        return

    # 2. Seleccionar red
    red = seleccionar_red(interfaces)
    if not red:
        return

    # 3. Escanear para encontrar Bastion
    bastion_ips = escanear_bastion(red['network_cidr'])
    if not bastion_ips:
        print("❌ No se encontró el Bastion en la red")
        return

    # 4. Conectar al Bastion
    username = input("Usuario del Bastion [cisco]: ").strip() or "cisco"
    password = input("Password del Bastion [cisco]: ").strip() or "cisco"

    tn = conectar_bastion(bastion_ips[0], username, password)
    if not tn:
        return

    # 5. Escanear red interna desde el Bastion
    red_interna = input("Red interna a escanear [192.168.0.0/24]: ").strip() or "192.168.0.0/24"
    dispositivos = escanear_red_desde_bastion(tn, red_interna)

    # 6. Mostrar resultados
    print(f"\n🎯 RESULTADOS DEL ESCANEO:")
    print("=" * 60)
    print(f"Red escaneada: {red_interna}")
    print(f"Dispositivos activos: {len(dispositivos)}")

    for dispositivo in dispositivos:
        print(f"   - {dispositivo}")

    # 7. Cerrar conexión
    tn.write(b"exit\n")
    tn.close()
    print("🔌 Conexión cerrada")


if __name__ == "__main__":
    # Agregar la carpeta modules al path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

    try:
        escaneo_inteligente()
    except KeyboardInterrupt:
        print("\n⏹️  Escaneo interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")