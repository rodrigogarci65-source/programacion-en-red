#!/usr/bin/env python3
import socket
import threading

PUERTO = 5000

def atender_cliente(conexion, direccion):
    print(f"[+] Cliente conectado desde {direccion}")
    buffer = ""
    try:
        while True:
            datos = conexion.recv(1024)
            if not datos:
                print(f"[i] Cliente {direccion} cerró la conexión ordenadamente.")
                break
            buffer += datos.decode("utf-8")
            while "\n" in buffer:
                linea, buffer = buffer.split("\n", 1)
                print(f"[{direccion}] Recibido: {linea}")
                respuesta = "ECO> " + linea + "\n"
                conexion.sendall(respuesta.encode("utf-8"))
    except (ConnectionResetError, BrokenPipeError):
        print(f"[!] El cliente {direccion} se desconectó abruptamente.")
    finally:
        conexion.close()
        print(f"[-] Conexión cerrada y registrada para {direccion}")

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("0.0.0.0", PUERTO))
servidor.listen(5)
print("Servidor persistente escuchando en puerto", PUERTO, "...")

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
    print("\nServidor detenido por el usuario.")
finally:
    servidor.close()
