#!/usr/bin/env python3
import socket

PUERTO = 5000
host = input("Host del servidor (Enter para localhost): ").strip() or "localhost"

try:
    cliente = socket.create_connection((host, PUERTO), timeout=5)
except socket.gaierror:
    print(f"[ERROR] No se pudo resolver el host '{host}'.")
    exit()
except ConnectionRefusedError:
    print(f"[ERROR] El servidor en {host}:{PUERTO} está apagado.")
    exit()

print(f"Conectado a {host}:{PUERTO}. Escribe mensajes (vacío para salir):")
buffer = ""
try:
    while True:
        mensaje = input("Tú> ")
        if mensaje == "":
            break
        cliente.sendall((mensaje + "\n").encode("utf-8"))
        while "\n" not in buffer:
            datos = cliente.recv(1024)
            if not datos:
                raise ConnectionResetError()
            buffer += datos.decode("utf-8")
        respuesta, buffer = buffer.split("\n", 1)
        print("Servidor>", respuesta)
except (ConnectionResetError, BrokenPipeError):
    print("[ERROR] El servidor se desconectó a media conversación.")
except KeyboardInterrupt:
    print("\nSalida forzada.")
finally:
    cliente.close()
    print("Cliente terminado.")
