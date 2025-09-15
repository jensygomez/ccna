# network_monitor/modules/ssh_manager/ssh_native.py

# network_monitor/modules/ssh_manager/ssh_native.py

import pexpect

def ssh_native_session(ip, username, password, hostname):
    """
    Abre una sesión SSH nativa como un túnel interactivo.
    Permite escribir comandos directamente en el dispositivo.
    La sesión se cierra al escribir 'exit' o 'logout'.
    """
    ssh_cmd = f"ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 " \
              f"-oHostKeyAlgorithms=+ssh-rsa {username}@{ip}"
    
    print(f"🌐 Abriendo sesión SSH nativa con {hostname}@{ip} ({ip})")
    print("👉 Escribe 'exit' o 'logout' para cerrar la sesión.\n")
    
    try:
        child = pexpect.spawn(ssh_cmd, encoding='utf-8', timeout=30)
        child.logfile = None  # para debug puedes usar sys.stdout

        # Manejo de fingerprint y password
        i = child.expect([
            "[Pp]assword:", 
            "Are you sure you want to continue connecting", 
            pexpect.EOF, 
            pexpect.TIMEOUT
        ])
        
        if i == 1:  # pregunta de fingerprint
            child.sendline("yes")
            child.expect("[Pp]assword:")

        if i in [0, 1]:  # pide password
            child.sendline(password)
        
        # Entrar en modo interactivo
        child.interact()  # 🔥 Mantiene la sesión abierta hasta que escribas exit/logout
        child.close()

    except Exception as e:
        print(f"❌ Error en sesión SSH nativa: {e}")
