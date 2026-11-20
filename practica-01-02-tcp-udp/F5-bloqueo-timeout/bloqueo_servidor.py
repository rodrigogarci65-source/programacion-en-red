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
print("servidor> cliente conectado:", direccion)
print("servidor> voy a llamar recv() (aqui me BLOQUEO hasta que llegue algo)")

inicio = time.time()
datos = conexion.recv(1024)
espera = time.time() - inicio

print("servidor> recv() regreso despues de {:.1f} segundos de espera".format(espera))
print("servidor> llego:", datos.decode("utf-8"))

conexion.close()
servidor.close()
