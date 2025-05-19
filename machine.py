from player import Player
from reel import *
from settings import *
from ui import UI
from wins import *
import pygame

class Machine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.win_animation_ongoing = False
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}

        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)

    def spawn_reels(self):
        x_topleft, y_topleft = 10, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft += (300 + X_OFFSET)
            self.reel_list[self.reel_index] = Reel((x_topleft, y_topleft))
            self.reel_index += 1

    def draw_reels(self, delta_time: float):
        for reel in self.reel_list.values():
            reel.animate(delta_time)

    def apply_server_message(self, msg: str):
        msg = msg.strip()
        parts = msg.split()
        if parts[0].startswith('win:'):
            payout = float(parts[0].split(':')[1])
            self.currPlayer.last_payout = payout
            self.currPlayer.total_won += payout
            self.win_animation_ongoing = True
            if len(parts) > 1 and parts[1].startswith('balance:'):
                self.currPlayer.balance = float(parts[1].split(':')[1])
        elif parts[0].startswith('balance:'):
            self.currPlayer.balance = float(parts[0].split(':')[1])
            self.currPlayer.last_payout = 0

    def cooldowns(self):
        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True
        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True
            self.spin_result = self.get_result()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
            self.toggle_spinning()

    def toggle_spinning(self):
        if self.can_toggle:
            self.spinning = not self.spinning
            self.can_toggle = False
            for reel in self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)

    def get_result(self):
        for reel in self.reel_list:
            self.spin_result[reel] = self.reel_list[reel].reel_spin_result()
        return self.spin_result

    def win_animation(self):
        if self.win_animation_ongoing:
            # Implemente sua animação baseada em self.currPlayer.last_payout
            pass

    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)
        # Desenha os símbolos dos rolos
        for reel in self.reel_list.values():
            reel.symbol_list.draw(self.display_surface)  # Adicione esta linha
        self.ui.update()
        self.win_animation()