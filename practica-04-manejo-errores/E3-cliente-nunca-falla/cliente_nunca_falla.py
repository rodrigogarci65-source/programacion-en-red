#!/usr/bin/env python3
import socket
import sys

PUERTO = 5000
ip_servidor = input("Ingresa la IP o host del servidor (ej. 127.0.0.1): ").strip()

if not ip_servidor:
    print("[ERROR] No ingresaste ninguna dirección IP.")
    sys.exit(1)

try:
    conexion = socket.create_connection((ip_servidor, PUERTO), timeout=5)
except socket.gaierror:
    print(f"[ERROR] IP o nombre de host inválido: '{ip_servidor}' no se puede resolver.")
    sys.exit(1)
except ConnectionRefusedError:
    print(f"[ERROR] El servidor en {ip_servidor}:{PUERTO} está apagado (conexión rechazada).")
    sys.exit(1)
except TimeoutError:
    print(f"[ERROR] Tiempo de espera agotado al intentar conectar con {ip_servidor}:{PUERTO}.")
    sys.exit(1)
except OSError as e:
    print(f"[ERROR] Fallo de red al conectar: {e}")
    sys.exit(1)

with conexion:
    conexion.settimeout(5)
    print(f"Conectado a {ip_servidor}:{PUERTO}. Escribe mensajes (vacío para salir):")
    try:
        while True:
            mensaje = input("Tú> ")
            if mensaje == "":
                break
            conexion.sendall((mensaje + "\n").encode("utf-8"))
            datos = conexion.recv(1024)
            if not datos:
                print("[ERROR] El servidor cerró la conexión a media conversación.")
                sys.exit(1)
            print("Servidor>", datos.decode("utf-8").strip())
    except TimeoutError:
        print("[ERROR] El servidor no respondió a tiempo (timeout).")
        sys.exit(1)
    except (ConnectionResetError, BrokenPipeError):
        print("[ERROR] El servidor se desconectó abruptamente a media conversación.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[INFO] Cliente cerrado por el usuario.")
        sys.exit(0)
