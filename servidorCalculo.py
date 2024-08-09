import socket

def enviarServidor(ip, puerto, lista):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, puerto))
            s.sendall(str(lista).encode())
            respuesta = s.recv(1024).decode()
            return int(respuesta)
    except Exception as e:
        print(f"Ocurrió un error al conectar con el servidor: {e}")
        return None

def procesarLista(lista):
    print(f"Servidor Coordinador recibió: {lista}")

    mitad = len(lista) // 2
    subLista1 = lista[:mitad]
    subLista2 = lista[mitad:]

    max1 = enviarServidor('localhost', 5001, subLista1)
    max2 = enviarServidor('localhost', 5002, subLista2)

    if max1 is None or max2 is None:
        print("Error: Uno o ambos servidores no respondieron correctamente.")
        return "Error: Servidor no disponible"

    max_value = max(max1, max2)
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
