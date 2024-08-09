import socket

def leer_archivo(nombre_archivo):
    try:
        with open(f'{nombre_archivo}.txt', 'r') as fichero:
            print(f"El archivo '{nombre_archivo}' ha sido abierto correctamente")
            return [int(line.strip()) for line in fichero.readlines()]
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no se ha podido abrir")
        return None

def enviar_datos_al_servidor(lista_datos):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
            cliente_socket.connect(('localhost', 5000))
            cliente_socket.sendall(str(lista_datos).encode())  # Enviar la lista como una cadena
            respuesta = cliente_socket.recv(1024).decode()
            return respuesta
    except Exception as e:
        print(f"Ocurrió un error al conectar con el servidor: {e}")
        return None

def main():
    print("¡BIENVENIDO!\nEncuentra el número mayor de tu lista")
    nomArchivo = input("Escribe el nombre de tu archivo: ")

    lista = leer_archivo(nomArchivo)
    if lista is not None:
        respuesta = enviar_datos_al_servidor(lista)
        if respuesta:
            print(f"El número mayor es: {respuesta}")

if __name__ == '__main__':
    main()
