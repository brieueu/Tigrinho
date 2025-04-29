import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Jogo do Tigrinho")

logo = pygame.image.load("assets/logo_free_background.png")
coin_sound = pygame.mixer.Sound("assets/coin_drop.mp3")

def mostrar_interface():
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(logo, (100, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    coin_sound.play()

        pygame.display.flip()

    pygame.quit()
    sys.exit()
