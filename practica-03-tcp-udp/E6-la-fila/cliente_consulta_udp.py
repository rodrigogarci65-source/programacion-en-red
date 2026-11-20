#!/usr/bin/env python3
import socket

DESTINO = ("localhost", 5001)
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.settimeout(3)

try:
    cliente.sendto("CUANTOS".encode("utf-8"), DESTINO)
    datos, _ = cliente.recvfrom(1024)
    print("Consulta UDP ->", datos.decode("utf-8").strip())
except socket.timeout:
    print("Sin respuesta UDP (timeout de 3s).")
finally:
    cliente.close()
