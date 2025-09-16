# NetMonDB/core/ssh_connector/main_ssh_connector.py



from .ssh_ssh_connector import connect_device

def ssh_main():
    """
    Función principal del módulo SSH.
    Devuelve el output crudo del dispositivo.
    """
    print("🔌 Conectando al dispositivo vía SSH...")
    # Aquí puedes pedir IP/usuario/contraseña o leer de .env
    host = input("IP del dispositivo: ")
    user = input("Usuario: ")
    password = input("Contraseña: ")

    output = connect_device(host, user, password, "show running-config")
    return output
