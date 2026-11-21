#!/usr/bin/env python3
import socket
import time

def consultar(servidor, mensaje, reintentos=3):
    """Envía una consulta UDP y reintenta con espera exponencial (1s, 2s, 4s)."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        cliente.settimeout(2)
        for intento in range(1, reintentos + 1):
            try:
                print(f"Intento {intento}/{reintentos}: enviando '{mensaje}'...")
                cliente.sendto((mensaje + "\n").encode("utf-8"), servidor)
                datos, _ = cliente.recvfrom(1024)
                return datos.decode("utf-8").strip()
            except TimeoutError:
                espera = 2 ** (intento - 1)
                print(f"Intento {intento}: sin respuesta. Esperando {espera}s...")
                time.sleep(espera)
    return None

DESTINO = ("127.0.0.1", 5001)
respuesta = consultar(DESTINO, "CUANTOS")
print("Respuesta:", respuesta if respuesta else "El servidor no respondió tras 3 intentos.")
