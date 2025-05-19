from settings import *
import pygame, random

class Reel:
    def __init__(self, pos):
        # Grupo de sprites para os símbolos no carretel
        self.symbol_list = pygame.sprite.Group()
        # Embaralha as chaves dos símbolos e limita a 5 para exibição
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5]  # Importa apenas quando há mais de 5 símbolos

        self.reel_is_spinning = False

        # Sons (opcionais)
        # self.stop_sound = pygame.mixer.Sound('audio/stop.mp3')
        # self.stop_sound.set_volume(0.5)

        # Popula o carretel com símbolos nas posições iniciais
        for idx, item in enumerate(self.shuffled_keys):
            self.symbol_list.add(Symbol(symbols[item], pos, idx))
            pos = list(pos)
            pos[1] += 300
            pos = tuple(pos)

    def animate(self, delta_time):
        if self.reel_is_spinning:
            # Atualiza os temporizadores de atraso e duração do giro
            self.delay_time -= (delta_time * 1000)
            self.spin_time  -= (delta_time * 1000)
            reel_is_stopping = False

            if self.spin_time < 0:
                reel_is_stopping = True

            # Inicia a animação de giro após o atraso
            if self.delay_time <= 0:
                for symbol in self.symbol_list:
                    # Move cada símbolo para baixo
                    symbol.rect.bottom += 100

                    # Quando o símbolo sai pela parte inferior, remove e gera um novo no topo
                    if symbol.rect.top == 1200:
                        if reel_is_stopping:
                            self.reel_is_spinning = False
                            # self.stop_sound.play()

                        symbol_idx = symbol.idx
                        symbol.kill()
                        # Adiciona símbolo aleatório no topo na mesma coluna
                        self.symbol_list.add(
                            Symbol(
                                symbols[random.choice(self.shuffled_keys)],
                                (symbol.x_val, -300),
                                symbol_idx
                            )
                        )

    def start_spin(self, delay_time):
        # Define o atraso antes de iniciar e o tempo total de giro
        self.delay_time = delay_time
        self.spin_time  = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        # Retorna a sequência de símbolos visíveis no carretel (índices do meio)
        resultado = []
        for i in GAME_INDICES:
            resultado.append(self.symbol_list.sprites()[i].sym_type)
        # Inverte a ordem para corresponder da parte de cima para baixo
        return resultado[::-1]

class Symbol(pygame.sprite.Sprite):
    def __init__(self, pathToFile, pos, idx):
        super().__init__()

        # Nome amigável do símbolo, extraído do nome do arquivo
        self.sym_type = pathToFile.split('/')[-1].split('.')[0]

        self.pos = pos
        self.idx = idx
        # Carrega a imagem e obtém o retângulo de colisão
        self.image = pygame.image.load(pathToFile).convert_alpha()
        self.rect  = self.image.get_rect(topleft=pos)
        self.x_val = self.rect.left

        # Parâmetros para animações de vitória
        self.size_x   = 300
        self.size_y   = 300
        self.alpha    = 255
        self.fade_out = False
        self.fade_in  = False

    def update(self):
        # Animação de crescimento para símbolos vencedores
        if self.fade_in:
            if self.size_x < 320:
                self.size_x += 1
                self.size_y += 1
                self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
        # Animação de desvanecimento para símbolos não vencedores
        elif self.fade_out:
            if self.alpha > 115:
                self.alpha -= 7
                self.image.set_alpha(self.alpha)
