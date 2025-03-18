#!/usr/bin/env python3
import socket
import threading

# Variável global que acumula os 10 reais apostados a cada jogada.
global_pot = 0
pot_lock = threading.Lock()  # Usado para garantir acesso sincronizado ao pot.

class ClientThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.money = 100   # Saldo inicial em reais
        self.coins = 0     # Saldo inicial em moedas
        self.running = True

    def run(self):
        welcome_msg = (
            "Bem-vindo ao jogo do Tigrinho!\n"
            "Você tem {} reais e {} moedas.\n"
            "Comandos disponíveis: 'play' (jogar), 'balance' (ver saldo) e 'quit' (sair).\n".format(self.money, self.coins)
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
                    self.conn.sendall("Comando não reconhecido. Use 'play', 'balance' ou 'quit'.\n".encode())
            except Exception as e:
                print("Erro com o cliente {}: {}".format(self.addr, e))
                break

        self.conn.close()

    def play_game(self):
        if self.money < 10:
            self.conn.sendall("Saldo insuficiente para jogar. Você precisa de pelo menos 10 reais.\n".encode())
            return

        # Custa 10 reais para jogar
        self.money -= 10
        self.conn.sendall("Você apostou 10 reais. Boa sorte!\n".encode())

        global global_pot
        win = False

        # Incrementa o pot de forma sincronizada
        with pot_lock:
            global_pot += 10
            # Se o pot atingir 200 (ou mais) reais, o jogador ganha 100 moedas e o pot é reiniciado.
            if global_pot >= 200:
                win = True
                global_pot = 0

        if win:
            self.coins += 100
            self.conn.sendall("Parabéns! O valor acumulado chegou a 200 reais.\nVocê ganhou 100 moedas!\n".encode())
        else:
            self.conn.sendall("Continue jogando... Valor atual acumulado: {} reais.\n".format(global_pot).encode())

    def send_balance(self):
        balance_msg = "Seu saldo: {} reais e {} moedas.\n".format(self.money, self.coins)
        self.conn.sendall(balance_msg.encode())

def main():
    host = ''  # Aceita conexões de qualquer endereço
    port = 5000  # Porta de escuta (pode ser alterada se necessário)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host, port))
    except Exception as e:
        print("Erro ao realizar bind na porta {}: {}".format(port, e))
        return

    server_socket.listen(5)
    print("Servidor rodando na porta {}. Aguardando conexões...".format(port))

    try:
        while True:
            conn, addr = server_socket.accept()
            print("Conexão estabelecida de {}:{}".format(addr[0], addr[1]))
            new_thread = ClientThread(conn, addr)
            new_thread.start()
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()
