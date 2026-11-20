#!/usr/bin/env python3
import socket

DESTINO = ("localhost", 5000)
MENSAJES = ["hola", "redes", "adios"]

cliente = socket.create_connection(DESTINO)
print("Conectado al servidor en", DESTINO)

buffer = ""
for mensaje in MENSAJES:
    cliente.sendall((mensaje + "\n").encode("utf-8"))
    while "\n" not in buffer:
        datos = cliente.recv(1024)
        if not datos:
            break
        buffer += datos.decode("utf-8")
    respuesta, buffer = buffer.split("\n", 1)
    print(f"Enviado: {mensaje} | Respuesta: {respuesta}")

cliente.close()
print("Cliente terminado.")
