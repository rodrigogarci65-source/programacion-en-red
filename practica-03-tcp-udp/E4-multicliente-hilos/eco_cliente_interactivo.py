#!/usr/bin/env python3
import socket

DESTINO = ("localhost", 5000)

cliente = socket.create_connection(DESTINO)
print("Conectado al servidor multicliente. Escribe mensajes (vacío para salir):")

buffer = ""
while True:
    mensaje = input("Tú> ")
    if mensaje == "":
        break
    cliente.sendall((mensaje + "\n").encode("utf-8"))
    while "\n" not in buffer:
        datos = cliente.recv(1024)
        if not datos:
            break
        buffer += datos.decode("utf-8")
    respuesta, buffer = buffer.split("\n", 1)
    print("Servidor>", respuesta)

cliente.close()
print("Desconectado.")
