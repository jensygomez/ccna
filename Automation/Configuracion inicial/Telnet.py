import getpass
import telnetlib
import time


HOST = "192.168.0.101"
user = input("Digite seu usuario: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST, timeout=10)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"configure terminal\n")
tn.write(b"interface loopback 0\n")
tn.write(b"ip address 1.1.1.1 255.255.255.0\n")
tn.write(b"end\n")
tn.write(b"wr\n")

print(tn.read_all().decode('ascii'))