#!/usr/bin/env python3
import socket

DESTINO = ("localhost", 5050)

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.settimeout(3)
print("Eco UDP. Escriba mensajes (vacio para salir).")

while True:
    mensaje = input("Usted dice: ")
    cliente.sendto(mensaje.encode("utf-8"), DESTINO)
    if mensaje == "":
        break
    try:
        datos, _ = cliente.recvfrom(1024)
        print("El servidor responde:", datos.decode("utf-8"))
    except socket.timeout:
        print("... silencio: el datagrama se perdio y NADIE aviso...")

cliente.close()
print("Conexion (bueno, no habia conexion) terminada.")
