#!/usr/bin/env python3
import socket

DESTINO = ("localhost", 5000)
apodo = input("Tu apodo para la fila: ").strip() or "anonimo"

try:
    cliente = socket.create_connection(DESTINO, timeout=5)
    cliente.sendall(f"TURNO>{apodo}\n".encode("utf-8"))
    buffer = ""
    while "\n" not in buffer:
        datos = cliente.recv(1024)
        if not datos:
            break
        buffer += datos.decode("utf-8")
    respuesta, _ = buffer.split("\n", 1)
    print("Respuesta del servidor:", respuesta)
    cliente.close()
except Exception as e:
    print("[ERROR TCP]", e)
