import pygame
from random import randint
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, DIE_SOUND
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.music_utils import play_sound


class ObstacleManager:
    def __init__(self):
        self.obstacles = []


    def update(self, game):

        obstacle_type = [
            Cactus(SMALL_CACTUS),
            Cactus(LARGE_CACTUS),
            Bird(),
        ]

        # se a lista de obstáculos estiver vazia, ele chama um índice aleatório do array de tipos de obstáculo
        if len(self.obstacles) == 0:
            self.obstacles.append(obstacle_type[randint(0, 2)])

        #faz a iteração pra cara elemento no array obstacles
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.hammer:
                    self.obstacles.remove(obstacle)
                    print(game.player.hammer)
                elif game.player.shield:
                    print(game.player.shield)
                    pass
                elif game.player.time_traveling:
                    pass
                else:
                    pygame.time.delay(500)
                    play_sound(DIE_SOUND)
                    game.playing = False
                    game.death_count += 1




    def clean_obstacles(self):
        self.obstacles = []

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
