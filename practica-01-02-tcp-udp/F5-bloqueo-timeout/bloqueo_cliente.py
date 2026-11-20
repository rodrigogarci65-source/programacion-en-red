#!/usr/bin/env python3
import socket
import time

ESPERA = 7
IP_SERVIDOR = "localhost"
PUERTO = 5199

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((IP_SERVIDOR, PUERTO))
print("cliente> conectado; voy a callar", ESPERA, "segundos antes de enviar...")
time.sleep(ESPERA)
cliente.send("ya llegue!".encode("utf-8"))
cliente.close()
