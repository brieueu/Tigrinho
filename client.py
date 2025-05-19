import socket
import threading
import pygame
import sys
from machine import Machine
from settings import *

def connect_to_server(host: str, port: int, on_message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    def listen():
        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    break
                on_message(data.decode())
            except:
                break
    threading.Thread(target=listen, daemon=True).start()
    return sock

class NetworkedGame:
    def __init__(self, host='127.0.0.1', port=4000):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Slot Machine Cliente')
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.machine = Machine()
        self.sock = connect_to_server(host, port, self.handle_server_message)  # Novo callback

    def handle_server_message(self, msg: str):
        """ Repassa mensagens do servidor para a Machine. """
        self.machine.apply_server_message(msg)
        print(f"Mensagem do servidor: {msg}")  # Debug

    def send_command(self, cmd: str):
        try:
            self.sock.sendall(cmd.encode())
        except Exception as e:
            print(f"Erro ao enviar '{cmd}':", e)

    def run(self):
        last_spin_time = 0
        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    self.send_command('quit')
                    pygame.quit()
                    sys.exit()
                # Espaço para girar rolos (sem deduzir saldo localmente)
                if evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
                    if self.machine.can_toggle and self.machine.currPlayer.balance >= self.machine.currPlayer.bet_size:
                        self.send_command('play')
                        last_spin_time = pygame.time.get_ticks()

            # Atualização do jogo
            dt = self.clock.tick(FPS) / 1000
            self.screen.blit(self.bg, (0,0))
            self.machine.update(dt)
            pygame.display.update()

if __name__ == '__main__':
    game = NetworkedGame(host='127.0.0.1', port=4000)
    game.run()
