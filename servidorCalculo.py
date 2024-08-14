import socket

def enviarServidor(ip, puerto, lista):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, puerto))
            s.sendall(str(lista).encode())
            respuesta = s.recv(1024).decode()
            return int(respuesta)
    except Exception as e:
        print(f"Ocurrió un error al conectar con el servidor {ip}:{puerto} - {e}")
        return None

def procesarLista(lista):
    print(f"Servidor Coordinador recibió: {lista}")

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
                return "Error: Servidores no disponibles"
        maximos.append(maximo)

    max_value = max(maximos)
    print(f"Servidor Coordinador encontró el valor máximo: {max_value}")

    return str(max_value)

def iniciarServidor():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
            servidor_socket.bind(('localhost', 5000))
            servidor_socket.listen(5)
            print("Servidor iniciado. Esperando conexiones...")

            while True:
                conexion, direccion = servidor_socket.accept()
                print(f"Conexión establecida con {direccion}")

                datos = conexion.recv(1024).decode()
                if datos:
                    print(f"Datos recibidos: {datos}")

                    lista = eval(datos)  

                    respuesta = procesarLista(lista)
                    conexion.sendall(respuesta.encode())

                conexion.close()

    except Exception as e:
        print(f"Ocurrió un error al conectar: {e}")

if __name__ == "__main__":
    iniciarServidor()
