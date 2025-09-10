# main_telnet.py (flujo simplificado)
import os
import sys
from modules.network_discovery import descubrir_redes_locales, seleccionar_red
from modules.bastion_scanner import escanear_bastion_manual, conectar_bastion
from modules.internal_scanner import escanear_red_desde_bastion


def escaneo_inteligente():
    """Flujo completo de escaneo inteligente"""
    print("🚀 INICIO DE ESCANEO INTELIGENTE")
    print("=" * 60)

    # 1. Mostrar redes disponibles (solo informativo)
    interfaces = descubrir_redes_locales()

    # 2. Conexión directa al Bastion
    bastion_info = escanear_bastion_manual()

    if not bastion_info:
        return

    # 3. Conectar al Bastion
    tn = conectar_bastion(
        bastion_info[0]['ip'],
        bastion_info[0]['username'],
        bastion_info[0]['password']
    )

    if not tn:
        return

    # 4. Escanear red interna desde el Bastion
    red_interna = input("Red interna a escanear [192.168.0.0/24]: ").strip() or "192.168.0.0/24"
    dispositivos = escanear_red_desde_bastion(tn, red_interna)

    # 5. Mostrar resultados
    print(f"\n🎯 RESULTADOS DEL ESCANEO:")
    print("=" * 60)
    print(f"Red escaneada: {red_interna}")
    print(f"Dispositivos activos: {len(dispositivos)}")

    for dispositivo in dispositivos:
        print(f"   - {dispositivo}")

    # 6. Cerrar conexión
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