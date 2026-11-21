#!/usr/bin/env python3
import threading
import time

def saludar(nombre, veces):
    for i in range(1, veces + 1):
        print(f"[{nombre}] Hola #{i}")
        time.sleep(0.5)

participantes = [("Ana", 3), ("Beto", 5), ("Cora", 2)]
hilos = []

for nombre, veces in participantes:
    hilo = threading.Thread(target=saludar, args=(nombre, veces))
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()

print("Todos los hilos terminaron.")
