#!/usr/bin/env python3
import socket

PUERTO = 5050

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("0.0.0.0", PUERTO))
servidor.listen(1)
print("Servidor eco escuchando en el puerto", PUERTO, "...")

# (a) Línea donde el servidor se bloquea esperando cliente:
conexion, direccion = servidor.accept()
print("Cliente conectado desde", direccion)

while True:
    # (b) Línea donde el servidor se bloquea esperando datos:
    datos = conexion.recv(1024)
    if not datos:
        break
    mensaje = datos.decode("utf-8")
    print("Me llego:", mensaje)
    eco = "ECO> " + mensaje
    conexion.send(eco.encode("utf-8"))

conexion.close()
servidor.close()
print("Servidor eco terminado.")
