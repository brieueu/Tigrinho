"mostrar na tela, usando o Pygame, as informações do jogador (saldo, valor da aposta e última vitória)"
from player import Player
from settings import *
import pygame, random

class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()

        try:
            # Carrega fontes para exibição de texto
            self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
            self.bet_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
            self.win_font = pygame.font.Font(UI_FONT, WIN_FONT_SIZE)
        except:
            # Mensagens de erro se a fonte não for encontrada
            print("Erro ao carregar fonte!")
            print(f"Atualmente, a variável UI_FONT está definida como {UI_FONT}")
            print("O arquivo existe?")
            quit()
        # Ângulo aleatório para o texto de vitória
        self.win_text_angle = random.randint(-4, 4)
        self.showing_win = False

    def clear_win_highlight(self):
        self.showing_win = False

    def update(self):
        # desenha HUD, saldo etc.
        self.draw_balance()
        # só desenha highlight de vitória se flag estiver ligada
        if self.showing_win:
            self.draw_win_combinations()

    def display_info(self):
        player_data = self.player.get_data()

        # Saldo e valor da aposta
        saldo_surf = self.font.render("Saldo: " + player_data['balance'], True, TEXT_COLOR, None)
        x, y = 20, self.display_surface.get_size()[1] - 30
        saldo_rect = saldo_surf.get_rect(bottomleft=(x, y))

        aposta_surf = self.bet_font.render("Aposta: " + player_data['bet_size'], True, TEXT_COLOR, None)
        x = self.display_surface.get_size()[0] - 20
        aposta_rect = aposta_surf.get_rect(bottomright=(x, y))

        # Desenha retângulos de fundo e adiciona texto
        pygame.draw.rect(self.display_surface, False, saldo_rect)
        pygame.draw.rect(self.display_surface, False, aposta_rect)
        self.display_surface.blit(saldo_surf, saldo_rect)
        self.display_surface.blit(aposta_surf, aposta_rect)

        # Exibe a última vitória, se houver
        if self.player.last_payout:
            ultimo_payout = player_data['last_payout']
            win_surf = self.win_font.render("WIN! R$" + ultimo_payout, True, TEXT_COLOR, None)
            x1 = 800
            y1 = self.display_surface.get_size()[1] - 60
            win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            win_rect = win_surf.get_rect(center=(x1, y1))
            self.display_surface.blit(win_surf, win_rect)

    def update(self):
        # Limpa a área inferior para redesenhar as informações
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 900, 1600, 100))
        self.display_info()