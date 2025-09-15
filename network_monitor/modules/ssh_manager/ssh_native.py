# network_monitor/modules/ssh_manager/ssh_native.py

import pexpect

def ssh_native_session(ip, username, password, hostname):
    """
    Abre una sesión SSH nativa con pexpect (con autocompletado/tab).
    """
    print(f"\n🌐 Abriendo sesión SSH nativa con {hostname} ({ip})")
    print("👉 Usa '.exit' para volver al menú principal.\n")

    try:
        ssh_cmd = f"ssh {username}@{ip}"
        child = pexpect.spawn(ssh_cmd)

        # Manejar password prompt
        child.expect("password:")
        child.sendline(password)

        # Transferir control total al usuario
        child.interact(escape_character=None)

        print("\n🔒 Sesión SSH cerrada.")
    except Exception as e:
        print(f"❌ Error en sesión SSH nativa: {e}")
