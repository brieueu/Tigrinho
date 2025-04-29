import socket

HOST = "localhost"
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Servidor ouvindo em {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"Conectado por {addr}")
    conn.sendall(b"Bem-vindo ao servidor do Tigrinho!")
    conn.close()
