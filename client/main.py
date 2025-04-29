import socket
from interface import mostrar_interface

def conectar_servidor():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 12345))
        print("Conectado ao servidor.")
        return client_socket
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return None

if __name__ == "__main__":
    socket_cliente = conectar_servidor()
    mostrar_interface()
