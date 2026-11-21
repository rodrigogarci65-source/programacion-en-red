#!/usr/bin/env python3
import socket

DESTINO = ("127.0.0.1", 5000)

with socket.create_connection(DESTINO, timeout=5) as c:
    print("1) Enviando mensaje fuera de protocolo...")
    c.sendall("HOLA_BASURA\n".encode("utf-8"))
    print("   Servidor respondió:", c.recv(1024).decode("utf-8").strip())

    print("2) Enviando bytes que no son UTF-8 válido...")
    c.sendall(b"\xff\xfe\xfd\n")
    print("   Servidor respondió:", c.recv(1024).decode("utf-8").strip())

print("Cliente basura terminado.")
