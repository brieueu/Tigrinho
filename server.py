#!/usr/bin/env python3
import socket
import threading
import random

# Variável global para sincronização
pot_lock = threading.Lock()

class ClientThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.money = 1000  # Saldo inicial em reais
        self.running = True

    def run(self):
        # Envia o saldo inicial
        self.conn.sendall(f"balance:{self.money}\n".encode())
        welcome_msg = (
            "Bem-vindo ao jogo do Tigrinho!\n"
            "Comandos: 'play', 'balance', 'quit'.\n"
        )
        self.conn.sendall(welcome_msg.encode())

        while self.running:
            try:
                data = self.conn.recv(1024)
                if not data:
                    break
                command = data.decode().strip().lower()

                if command == "play":
                    self.play_game()
                elif command == "balance":
                    self.send_balance()
                elif command == "quit":
                    self.conn.sendall("Saindo do jogo. Até mais!\n".encode())
                    self.running = False
                else:
                    self.conn.sendall("Comando inválido.\n".encode())
            except Exception as e:
                print(f"Erro com {self.addr}: {e}")
                break
        self.conn.close()

    def play_game(self):
        if self.money < 10:
            self.conn.sendall("Saldo insuficiente. Mínimo 10 reais.\n".encode())
            return

        # Deduz aposta e verifica vitória
        self.money -= 10
        win = random.random() < 0.3  #30% chance de vitória, mas pode ser alterado
        if win:
            payout = 50  # Valor exemplo
            self.money += payout
            self.conn.sendall(f"win:{payout} balance:{self.money}\n".encode())
        else:
            self.conn.sendall(f"balance:{self.money}\n".encode())

    def send_balance(self):
        self.conn.sendall(f"Saldo atual: {self.money} reais.\n".encode())

def main():
    host = ''
    port = 4000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Servidor rodando na porta {port}...")
        while True:
            conn, addr = server_socket.accept()
            print(f"Conexão de {addr[0]}:{addr[1]}")
            ClientThread(conn, addr).start()
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()
