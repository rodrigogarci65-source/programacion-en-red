#!/usr/bin/env python3
import socket

PUERTO = 5001

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(("0.0.0.0", PUERTO))
print("Servidor UDP escuchando en puerto", PUERTO, "...")

while True:
    datos, direccion = servidor.recvfrom(1024)
    mensaje = datos.decode("utf-8").strip()
    print(f"Datagrama de {direccion}: {mensaje}")
    if mensaje == "ESTADO":
        servidor.sendto("servidor activo".encode("utf-8"), direccion)
