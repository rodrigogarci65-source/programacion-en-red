#!/usr/bin/env python3
import socket

DESTINO = ("127.0.0.1", 5000)
apodo = input("Apodo: ").strip() or "anonimo"

with socket.create_connection(DESTINO, timeout=5) as c:
    c.sendall(f"TURNO>{apodo}\n".encode("utf-8"))
    print("Respuesta:", c.recv(1024).decode("utf-8").strip())
