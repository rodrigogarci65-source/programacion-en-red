#!/usr/bin/env python3
import socket

IP_SERVIDOR = "localhost"
PUERTO = 9000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((IP_SERVIDOR, PUERTO))
cliente.send("Prueba de codigo limpio!".encode("utf-8"))
cliente.close()
