import socket
import threading

def max_in_subarray(data):
    return max(data)

def manejar_conexion(conn, addr, port):
    """ Función para manejar cada conexión de cliente en un hilo separado """
    with conn:
        try:
            print(f"Conectado por {addr}")
            data = conn.recv(1024)
            if data:
                subarray = eval(data.decode())  
                print(f"Servidor de Operación {port} recibió el subarreglo: {subarray}")
                max_value = max_in_subarray(subarray)
                print(f"Servidor de Operación {port} encontró el valor máximo: {max_value}")
                conn.sendall(str(max_value).encode())
        except Exception as e:
            print(f"Error en el servidor {port}: {e}")
            conn.sendall("Error")
        finally:
            conn.close()

def server_operacion(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        print(f"Servidor de Operación escuchando en el puerto {port}")
        while True:
            conn, addr = s.accept()
            
            hilo = threading.Thread(target=manejar_conexion, args=(conn, addr, port))
            hilo.start()

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1])
    server_operacion(port)
