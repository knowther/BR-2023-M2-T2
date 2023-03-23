import pygame
from random import randint
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, DIE_SOUND, SHIELD_SOUND, HAMMER_SOUND
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
                #os demais sons estão aqui porque o importante é tocar quando colidir com objeto
                if game.player.hammer:
                    self.obstacles.remove(obstacle)
                    play_sound(HAMMER_SOUND)
                elif game.player.shield:
                    play_sound(SHIELD_SOUND)
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
