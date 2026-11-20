#!/usr/bin/env python3
import socket

# Constantes en MAYÚSCULAS para evitar números o textos mágicos
DIRECCION_LOCAL = "localhost"
PUERTO = 9000
TAMANO_BUFFER = 1024

# Se crea el socket TCP sobre IPv4
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permite reutilizar el puerto inmediatamente sin esperar al sistema operativo
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Asocia el servidor a una dirección y puerto conocidos para que el cliente lo encuentre
servidor.bind((DIRECCION_LOCAL, PUERTO))
servidor.listen(1)
print("Servidor limpio escuchando en el puerto", PUERTO, "...")

# accept() bloquea hasta que llegue un cliente y devuelve un socket NUEVO para conversar
conexion, direccion_cliente = servidor.accept()
print("Cliente conectado desde:", direccion_cliente)

# Recibe hasta 1024 bytes y los decodifica de bytes a texto legible en UTF-8
datos_recibidos = conexion.recv(TAMANO_BUFFER)
mensaje_texto = datos_recibidos.decode("utf-8")
print("Me llego:", mensaje_texto)

# Se cierran ambos sockets (primero el de conversación y luego el de escucha)
conexion.close()
servidor.close()
