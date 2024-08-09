import socket

def max_in_subarray(data):
    return max(data)

def server_operacion(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        print(f"Servidor de Operación escuchando en el puerto {port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conectado por {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                subarray = eval(data.decode())
                print(f"Servidor de Operación {port} recibió el subarreglo: {subarray}")
                max_value = max_in_subarray(subarray)
                print(f"Servidor de Operación {port} encontró el valor máximo: {max_value}")
                conn.sendall(str(max_value).encode())

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1])
    server_operacion(port)
