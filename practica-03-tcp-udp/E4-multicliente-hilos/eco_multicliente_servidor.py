#!/usr/bin/env python3
import socket
import threading

PUERTO = 5000

def atender_cliente(conexion, direccion):
    print(f"[+] Cliente conectado desde {direccion}")
    buffer = ""
    while True:
        datos = conexion.recv(1024)
        if not datos:
            break
        buffer += datos.decode("utf-8")
        while "\n" in buffer:
            linea, buffer = buffer.split("\n", 1)
            print(f"[{direccion}] Recibido: {linea}")
            respuesta = "ECO> " + linea + "\n"
            conexion.sendall(respuesta.encode("utf-8"))
    conexion.close()
    print(f"[-] Cliente desconectado: {direccion}")

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("0.0.0.0", PUERTO))
servidor.listen(5)
print("Servidor multicliente TCP escuchando en puerto", PUERTO, "...")

while True:
    conexion, direccion = servidor.accept()
    hilo = threading.Thread(
        target=atender_cliente,
        args=(conexion, direccion),
        daemon=True
    )
    hilo.start()
