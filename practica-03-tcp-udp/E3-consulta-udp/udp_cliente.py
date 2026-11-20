#!/usr/bin/env python3
import socket

DESTINO = ("localhost", 5001)

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.settimeout(3)

try:
    cliente.sendto("ESTADO".encode("utf-8"), DESTINO)
    datos, _ = cliente.recvfrom(1024)
    print("Respuesta del servidor:", datos.decode("utf-8"))
except socket.timeout:
    print("Sin respuesta: el servidor no contestó en 3 segundos.")
finally:
    cliente.close()
