import pygame

from dino_runner.utils.constants import SMALL_CACTUS
from dino_runner.components.obstacles.cactus import Cactus


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
<<<<<<< HEAD

    def update(self, game):
        if len(self.obstacles) == 0:
            self.obstacles.append(Cactus(SMALL_CACTUS))
=======


    def update(self, game):

        obstacle_type = [
            Cactus(SMALL_CACTUS),
            Cactus(LARGE_CACTUS),
            Bird(),
        ]

        # se a lista de obstáculos estiver vazia, ele chama um índice aleatório do array de tipos de obstáculo
        if len(self.obstacles) == 0:
            self.obstacles.append(obstacle_type[randint(0, 2)])
>>>>>>> adab659 (aula 3 sincrona)

        #faz a iteração pra cara elemento no array obstacles
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False



    def clean_obstacles(self):
        self.obstacles = []

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)