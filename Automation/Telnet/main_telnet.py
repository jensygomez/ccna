# main_telnet.py (versión corregida)
import os
import sys

# Importaciones globales
from modules.network_discovery import descubrir_redes_locales, mostrar_redes
from modules.bastion_scanner import escanear_bastion_manual, conectar_bastion
from modules.internal_scanner import mostrar_y_seleccionar_red, escanear_red_desde_bastion

def main():
    """Función principal"""
    print("🚀 Iniciando Telnet Manager...")
    print("📂 Directorio actual:", os.getcwd())

    # Agregar la carpeta modules al path
    modules_path = os.path.join(os.path.dirname(__file__), 'modules')
    print("📁 Ruta de módulos:", modules_path)
    sys.path.append(modules_path)

    try:
        print("✅ Módulos importados correctamente")
        escaneo_inteligente()

    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("📋 Contenido de la carpeta modules:")
        if os.path.exists(modules_path):
            for file in os.listdir(modules_path):
                if file.endswith('.py'):
                    print(f"   - {file}")
        else:
            print("   ❌ La carpeta modules no existe")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

def escaneo_inteligente():
    """Flujo completo de escaneo inteligente"""
    print("\n" + "=" * 60)
    print("🚀 INICIO DE ESCANEO INTELIGENTE")
    print("=" * 60)

    # 1. Descubrir redes locales (solo informativo)
    redes = descubrir_redes_locales()
    mostrar_redes(redes)  # Mostrar información de redes

    # 2. Conexión al Bastion
    print("\n🔗 Conectando al Bastion...")
    bastion_info = escanear_bastion_manual()

    if not bastion_info:
        print("❌ No se pudo obtener información del Bastion")
        return

    # 3. Conectar al Bastion
    tn = conectar_bastion(
        bastion_info[0]['ip'],
        bastion_info[0]['username'],
        bastion_info[0]['password']
    )

    if not tn:
        print("❌ No se pudo conectar al Bastion")
        return

    # 4. Selección de red desde BD
    print("\n📊 Consultando base de datos...")
    red_interna = mostrar_y_seleccionar_red()

    # 5. Escanear red interna desde el Bastion
    print("\n🔍 Escaneando red interna...")
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
    main()