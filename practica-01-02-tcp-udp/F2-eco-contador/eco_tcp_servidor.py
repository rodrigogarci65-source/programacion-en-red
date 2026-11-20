#!/usr/bin/env python3
import socket

PUERTO = 5050

def armar_eco(mensaje, numero):
    """Devuelve el mensaje formateado con el número de eco."""
    return "ECO #" + str(numero) + "> " + mensaje

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("0.0.0.0", PUERTO))
servidor.listen(1)
print("Servidor eco F2 escuchando en el puerto", PUERTO, "...")

conexion, direccion = servidor.accept()
print("Cliente conectado desde", direccion)

contador = 0
while True:
    datos = conexion.recv(1024)
    if not datos:
        break
    contador += 1
    mensaje = datos.decode("utf-8")
    print(f"Mensaje #{contador} recibido:", mensaje)
    eco = armar_eco(mensaje, contador)
    conexion.send(eco.encode("utf-8"))

conexion.close()
servidor.close()
print("Servidor eco terminado.")
