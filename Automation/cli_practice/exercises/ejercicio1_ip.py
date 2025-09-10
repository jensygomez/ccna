import os
import datetime

LOG_FILE = os.path.join("..", "logs", "ejercicio1_log.txt")

def log_attempt(command, result):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} | Comando: {command} | Resultado: {result}\n")

def validate_command(user_command, expected_command):
    return " ".join(user_command.strip().split()).lower() == expected_command.lower()

def ejecutar():
    print("\n=== Ejercicio 1: Configurar IP ===")
    print("Modo: Router(config-if)#")
    print("Objetivo: ip address 192.168.1.1 255.255.255.0")

    expected_command = "ip address 192.168.1.1 255.255.255.0"

    while True:
        cmd = input("Router(config-if)# ").strip()
        if cmd.lower() == "exit":
            print("🔹 Saliendo del ejercicio...")
            break
        elif validate_command(cmd, expected_command):
            print("✅ ¡Perfecto! Comando correcto.")
            log_attempt(cmd, "Correcto")
            break
        else:
            print("❌ Comando incorrecto. Pista: empieza con 'ip address'.")
            log_attempt(cmd, "Incorrecto")
