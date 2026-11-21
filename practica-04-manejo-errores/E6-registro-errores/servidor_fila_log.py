#!/usr/bin/env python3
import socket
import threading
import time

PUERTO_TCP = 5000
PUERTO_UDP = 5001
ARCHIVO_LOG = "errores.log"

contador_turnos = 0
candado = threading.Lock()

def registrar_error(direccion, descripcion):
    marca_tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
    linea = f"{marca_tiempo} {direccion} {descripcion}\n"
    with candado:
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
            f.write(linea)
    print(f"[LOG] {linea.strip()}")

def atender_cliente_tcp(conexion, direccion):
    global contador_turnos
    print(f"[TCP +] Conectado {direccion}")
    buffer = ""
    try:
        with conexion:
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    break
                try:
                    texto = datos.decode("utf-8")
                except UnicodeDecodeError:
                    registrar_error(direccion, "bytes que no son UTF-8 válido")
                    conexion.sendall("ERROR> Codificación UTF-8 inválida\n".encode("utf-8"))
                    continue

                buffer += texto
                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)
                    linea = linea.strip()
                    if linea.startswith("TURNO>"):
                        apodo = linea.split(">", 1)[1].strip() or "anonimo"
                        with candado:
                            contador_turnos += 1
                            mi_turno = contador_turnos
                        conexion.sendall(f"turno>{mi_turno}\n".encode("utf-8"))
                        print(f"[TCP] Turno #{mi_turno} asignado a '{apodo}' ({direccion})")
                    else:
                        registrar_error(direccion, f"mensaje fuera de protocolo: '{linea}'")
                        conexion.sendall("ERROR> Formato inválido. Usa TURNO>apodo\n".encode("utf-8"))
    except ConnectionResetError:
        registrar_error(direccion, "conexión reiniciada por el cliente")
    except BrokenPipeError:
        registrar_error(direccion, "tubería rota al intentar responder")
    finally:
        print(f"[TCP -] Conexión cerrada: {direccion}")

def ciclo_udp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor_udp:
        servidor_udp.bind(("0.0.0.0", PUERTO_UDP))
        print(f"[UDP] Escuchando consultas en puerto {PUERTO_UDP} ...")
        while True:
            try:
                datos, direccion = servidor_udp.recvfrom(1024)
                mensaje = datos.decode("utf-8").strip()
                if mensaje == "CUANTOS":
                    with candado:
                        total = contador_turnos
                    servidor_udp.sendto(f"van>{total}\n".encode("utf-8"), direccion)
            except UnicodeDecodeError:
                registrar_error(direccion, "datagrama UDP con bytes no UTF-8")
            except OSError as e:
                registrar_error(("UDP", PUERTO_UDP), f"error de socket: {e}")

hilo_udp = threading.Thread(target=ciclo_udp, daemon=True)
hilo_udp.start()

servidor_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    servidor_tcp.bind(("0.0.0.0", PUERTO_TCP))
except OSError:
    print(f"[ERROR] El puerto {PUERTO_TCP} ya está ocupado.")
    exit(1)

servidor_tcp.listen(10)
print(f"[TCP] Servidor LA FILA con log escuchando en puerto {PUERTO_TCP} ...")

try:
    while True:
        conexion, direccion = servidor_tcp.accept()
        hilo = threading.Thread(target=atender_cliente_tcp, args=(conexion, direccion), daemon=True)
        hilo.start()
except KeyboardInterrupt:
    print("\nServidor detenido.")
finally:
    servidor_tcp.close()
