import telnetlib

HOST = "192.168.1.2"
USER = "admin"
PASSWORD = "cisco"

tn = telnetlib.Telnet(HOST)
tn.read_until(b'Password:')
tn.write(PASSWORD.encode('ascii') + b"\n")

tn.write(b"enable\n")
tn.write(b"cisco\n")
tn.write(b"configure terminal\n")
tn.write(b"hostname Sucursal_01\n")
tn.write(b"end\n")
tn.write(b"wr\n")
tn.write(b"\n")

print(tn.read_all().decode('asscii'))
tn.close()