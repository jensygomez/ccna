# main_telnet.py (parte modificada)
from modules.internal_scanner import mostrar_y_seleccionar_red, escanear_red_desde_bastion


def escaneo_inteligente():
    """Flujo completo de escaneo inteligente"""
    print("🚀 INICIO DE ESCANEO INTELIGENTE")
    print("=" * 60)

    # 1. Mostrar redes disponibles (solo informativo)
    from modules.network_discovery import descubrir_redes_locales
    interfaces = descubrir_redes_locales()

    # 2. Conexión al Bastion
    from modules.bastion_scanner import escanear_bastion_manual, conectar_bastion
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

    # 4. SELECCIÓN DE RED DESDE BD (NUEVO)
    red_interna = mostrar_y_seleccionar_red()

    # 5. Escanear red interna desde el Bastion
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