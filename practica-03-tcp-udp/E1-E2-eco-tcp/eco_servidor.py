#!/usr/bin/env python3
import socket

PUERTO = 5000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("0.0.0.0", PUERTO))
servidor.listen(1)
print("Servidor eco TCP escuchando en puerto", PUERTO, "...")

conexion, direccion = servidor.accept()
print("Cliente conectado desde:", direccion)

buffer = ""
while True:
    datos = conexion.recv(1024)
    if not datos:
        break
    buffer += datos.decode("utf-8")
    while "\n" in buffer:
        linea, buffer = buffer.split("\n", 1)
        print("Recibido:", linea)
        respuesta = "ECO> " + linea + "\n"
        conexion.sendall(respuesta.encode("utf-8"))

conexion.close()
servidor.close()
print("Servidor terminado.")
