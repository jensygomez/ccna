"""
Módulo para verificar conexión al switch - Versión simplificada
"""
from netmiko import ConnectHandler

# Configuración del dispositivo
device_config = {
    'device_type': 'cisco_ios',
    'host': '192.168.100.10',      # Cambia por la IP de tu switch
    'username': 'admin',        # Cambia por tu usuario
    'password': '1234',     # Cambia por tu contraseña
    'secret': '1234',         # Cambia por tu enable secret (si tiene)
}

def test_connection_menu():
    """Menú para probar conexión al switch"""
    print("\n🔍 PROBAR CONEXIÓN AL SWITCH")
    print(f"Intentando conectar a: {device_config['host']}")
    
    try:
        # Intentar conexión
        connection = ConnectHandler(**device_config)
        
        # Intentar entrar en modo enable si hay secret
        if device_config.get('secret'):
            connection.enable()
            print("✅ Modo enable: OK")
        
        # Verificar conexión con comando simple
        test_output = connection.send_command('show version', read_timeout=10)
        print("✅ Comando ejecutado correctamente")
        
        # Cerrar conexión
        connection.disconnect()
        print("✅ Conexión cerrada correctamente")
        print(f"\n🎉 ¡Conexión exitosa a {device_config['host']}!")
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
    
    from modules.menu_operations import press_enter_to_continue
    press_enter_to_continue()
