import getpass
import telnetlib

HOST = "192.168.0.101"
user = input("Digite seu usuario: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

print("se conectó correctamente")

print(tn.read_all().decode('ascii'))