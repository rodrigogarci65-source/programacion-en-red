#!/usr/bin/env python3
import socket
import threading

PUERTO_TCP = 5000
PUERTO_UDP = 5001

contador_turnos = 0
candado = threading.Lock()

def atender_cliente_tcp(conexion, direccion):
    global contador_turnos
    print(f"[TCP +] Conectado {direccion}")
    buffer = ""
    try:
        while True:
            datos = conexion.recv(1024)
            if not datos:
                break
            buffer += datos.decode("utf-8")
            while "\n" in buffer:
                linea, buffer = buffer.split("\n", 1)
                linea = linea.strip()
                if linea.startswith("TURNO>"):
                    apodo = linea.split(">", 1)[1].strip()
                    with candado:
                        contador_turnos += 1
                        mi_turno = contador_turnos
                    respuesta = f"turno>{mi_turno}\n"
                    conexion.sendall(respuesta.encode("utf-8"))
                    print(f"[TCP] Turno #{mi_turno} asignado a '{apodo}' ({direccion})")
                else:
                    conexion.sendall("ERROR> Formato invalido. Usa TURNO>apodo\n".encode("utf-8"))
    except (ConnectionResetError, BrokenPipeError, UnicodeDecodeError):
        print(f"[TCP !] Error o desconexión abrupta de {direccion}")
    finally:
        conexion.close()
        print(f"[TCP -] Cerrada conexión de {direccion}")

def ciclo_udp():
    servidor_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_udp.bind(("0.0.0.0", PUERTO_UDP))
    print(f"[UDP] Escuchando consultas en puerto {PUERTO_UDP} ...")
    while True:
        try:
            datos, direccion = servidor_udp.recvfrom(1024)
            mensaje = datos.decode("utf-8").strip()
            if mensaje == "CUANTOS":
                with candado:
                    total = contador_turnos
                respuesta = f"van>{total}\n"
                servidor_udp.sendto(respuesta.encode("utf-8"), direccion)
                print(f"[UDP] Consulta de {direccion} -> respondido: van>{total}")
        except Exception as e:
            print(f"[UDP !] Error ignorado: {e}")

# Hilo independiente para el ciclo UDP
hilo_udp = threading.Thread(target=ciclo_udp, daemon=True)
hilo_udp.start()

# Ciclo principal TCP
servidor_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor_tcp.bind(("0.0.0.0", PUERTO_TCP))
servidor_tcp.listen(10)
print(f"[TCP] Servidor LA FILA escuchando en puerto {PUERTO_TCP} ...")

try:
    while True:
        conexion, direccion = servidor_tcp.accept()
        hilo = threading.Thread(
            target=atender_cliente_tcp,
            args=(conexion, direccion),
            daemon=True
        )
        hilo.start()
except KeyboardInterrupt:
    print("\nServidor LA FILA detenido.")
finally:
    servidor_tcp.close()
