import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH


class Obstacle(Sprite):
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed, obstacles):
        #essa parte aqui vai reduzindo o valor no eixo x de acordo com o valor de game speed, ex: game speed = 20
        #a cada frame ele vai reduzindo 20 até chegar no final da tela
        self.rect.x -= game_speed

        #quando a imagem chega no final, ela é removida
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], (self.rect.x, self.rect.y))