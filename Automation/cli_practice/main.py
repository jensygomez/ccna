import os
import datetime

# Ruta donde guardaremos los logs
LOG_FILE = os.path.join("logs", "practice_log.txt")

# Función para registrar en log
def log_attempt(command, result):
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.datetime.now()} | Comando: {command} | Resultado: {result}\n")

# Función que valida el comando
def validate_command(user_command, expected_command):
    # Eliminamos espacios extra
    user_command = " ".join(user_command.strip().split())
    if user_command.lower() == expected_command.lower():
        return True
    return False

def main():
    os.makedirs("logs", exist_ok=True)

    print("="*55)
    print(" 🧩 Ejercicio 1: Configurar la IP de una interfaz en un router ")
    print("="*55)
    print("\nEstás en el modo de configuración de interfaz:")
    print("Router(config-if)# ")
    print("Objetivo: Configura la IP 192.168.1.1 con máscara 255.255.255.0\n")

    expected_command = "ip address 192.168.1.1 255.255.255.0"

    while True:
        user_command = input("Router(config-if)# ").strip()

        if user_command.lower() == "exit":
            print("\n🔹 Saliendo del ejercicio...")
            break

        if validate_command(user_command, expected_command):
            print("✅ ¡Perfecto! El comando está bien escrito.")
            log_attempt(user_command, "Correcto")
            break
        else:
            print("❌ Comando incorrecto.")
            print("💡 Pista: El comando empieza con 'ip address'.")
            log_attempt(user_command, "Incorrecto")

if __name__ == "__main__":
    main()
