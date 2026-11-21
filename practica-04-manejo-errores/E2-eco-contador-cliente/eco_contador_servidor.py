#!/usr/bin/env python3
import socket
import threading

PUERTO = 5000

def atender_cliente(conexion, direccion):
    print(f"[+] Cliente conectado: {direccion}")
    contador = 0  # Local al hilo: cada cliente lleva su propia cuenta
    buffer = ""
    try:
        with conexion:
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    break
                buffer += datos.decode("utf-8")
                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)
                    contador += 1
                    respuesta = f"{contador}>{linea}\n"
                    print(f"[{direccion}] Mensaje #{contador}: {linea}")
                    conexion.sendall(respuesta.encode("utf-8"))
    except (ConnectionResetError, BrokenPipeError):
        print(f"[!] Cliente {direccion} se desconectó abruptamente.")
    finally:
        print(f"[-] Conexión cerrada: {direccion}")

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    servidor.bind(("0.0.0.0", PUERTO))
except OSError:
    print(f"[ERROR] El puerto {PUERTO} está ocupado.")
    exit(1)

servidor.listen(5)
print(f"Servidor eco con contador por cliente escuchando en puerto {PUERTO} ...")

try:
    while True:
        conexion, direccion = servidor.accept()
        hilo = threading.Thread(
            target=atender_cliente,
            args=(conexion, direccion),
            daemon=True
        )
        hilo.start()
except KeyboardInterrupt:
    print("\nServidor detenido.")
finally:
    servidor.close()
