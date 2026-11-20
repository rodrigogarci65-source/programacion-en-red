#!/usr/bin/env python3
import socket

IP_SERVIDOR = "localhost"
PUERTO = 5061

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((IP_SERVIDOR, PUERTO))

# Tres mensajes viajan JUNTOS en un mismo send() separados por \n
cliente.send("primer mensaje\nsegundo mensaje\ntercer mensaje\n".encode("utf-8"))
print("cliente framing> tres mensajes enviados en un solo send().")

cliente.close()
