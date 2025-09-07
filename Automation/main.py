import telnetlib
import time

HOST = "192.168.1.2"
PASSWORD = "cisco"

tn = telnetlib.Telnet(HOST)

# Login
tn.read_until(b"Password:")
tn.write(PASSWORD.encode('ascii') + b"\n")

# Enable mode
tn.write(b"enable\n")
tn.read_until(b"Password:")
tn.write(b"cisco\n")

# Configuración
tn.write(b"configure terminal\n")
tn.write(b"hostname Sucursal_01\n")
tn.write(b"end\n")
tn.write(b"write memory\n")
tn.write(b"\n")

# Dar tiempo a que el switch responda
time.sleep(1)

# Leer toda la salida
output = tn.read_very_eager().decode('ascii')
print(output)

tn.close()
