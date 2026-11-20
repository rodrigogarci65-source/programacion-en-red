#!/usr/bin/env python3
import socket
import time

PUERTO = 5199

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("localhost", PUERTO))
servidor.listen(1)
print("servidor> esperando conexion...")

conexion, direccion = servidor.accept()
conexion.settimeout(5)
print("servidor> cliente conectado:", direccion)
print("servidor> voy a llamar recv() con timeout de 5s...")

inicio = time.time()
try:
    datos = conexion.recv(1024)
    espera = time.time() - inicio
    print("servidor> recv() regreso despues de {:.1f} segundos de espera".format(espera))
    print("servidor> llego:", datos.decode("utf-8"))
except socket.timeout:
    espera = time.time() - inicio
    print("servidor> EXCEPCION socket.timeout despues de {:.1f} segundos!".format(espera))

conexion.close()
servidor.close()
