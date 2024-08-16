import socket

def calculo_falla(lista):
    print("Servidor Calculo procede a realizar la operación por su cuenta")
    print(f"El numero mayor de la lista es {max(lista)}")
    return str(max(lista))


def enviarServidor(ip, puerto, lista):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, puerto))
            s.sendall(str(lista).encode())
            respuesta = s.recv(1024).decode()
            return int(respuesta)
    except socket.timeout:
            print(f"Error: Conexión con {ip}:{puerto} agotó el tiempo.")
    except Exception as e:
        print(f"Ocurrió un error al conectar con el servidor {ip}:{puerto} - {e}")
        return None

def procesarLista(lista):
    print(f"Servidor Calculo recibió: {lista}")

    mitad = len(lista) // 2
    subLista1 = lista[:mitad]
    subLista2 = lista[mitad:]

    servidores = [
        {'ip': 'localhost', 'puerto': 5001, 'sublista': subLista1},
        {'ip': 'localhost', 'puerto': 5002, 'sublista': subLista2}
    ]

    maximos = []
    for servidor in servidores:
        maximo = enviarServidor(servidor['ip'], servidor['puerto'], servidor['sublista'])
        if maximo is None:
            # Reintentar con el otro servidor si uno falla
            print(f"Intentando con el otro servidor para el subarreglo {servidor['sublista']}")
            otro_servidor = [s for s in servidores if s != servidor][0]
            maximo = enviarServidor(otro_servidor['ip'], otro_servidor['puerto'], servidor['sublista'])
            if maximo is None:
                print("Error: Ambos servidores fallaron.")
                return "sin_servidores_disponibles"
        maximos.append(maximo)

    max_value = max(maximos)
    print(f"Servidor Calculo encontró el valor máximo: {max_value}")

    return str(max_value)

def iniciarServidor():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
            servidor_socket.bind(('localhost', 5000))
            servidor_socket.listen()
            print("Servidor iniciado. Esperando conexiones...")

            while True:
                conexion, direccion = servidor_socket.accept()
                print(f"Conexión establecida con {direccion}")

                try:
                    datos = conexion.recv(1024).decode()
                    if datos:
                        print(f"Datos recibidos: {datos}")

                        lista = eval(datos)  

                        respuesta = procesarLista(lista)

                        if(respuesta == "sin_servidores_disponibles"):
                            respuesta = calculo_falla(lista)

                        conexion.sendall(respuesta.encode())
                except Exception as e:
                    print(f"Error durante el procesamiento de la solicitud: {e}")
                finally:
                    conexion.close()

    except Exception as e:
        print(f"Ocurrió un error al conectar: {e}")

if __name__ == "__main__":
    iniciarServidor()
