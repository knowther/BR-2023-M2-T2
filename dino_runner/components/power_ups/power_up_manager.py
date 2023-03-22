import random
import pygame

from dino_runner.components.power_ups.shield import Shield


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0

        #classe que serve pra controlar quando o poder deve aparecer
    def generate_power_up(self, score):
        #se a lista de powerup estiver vazia, ele define quando o powerup vai aparecer +
        #no início da partida essa condição já é atendida e ele já define em que momento do jogo o power_up vai aparecer, quando a condição é atendida+
        # o jogo redefine essa variável para 200/300 acima do que foi definida anteriormente pra sempre ir atualizando o valor de quando o powerup aparece
        if len(self.power_ups) == 0 and self.when_appears == score:
            #aqui escolhe um valor randômico entre 200 e 300 e incrementa no when_appears para o powerup aparecer após atingir essa nova pontuação
            self.when_appears += random.randint(200,300)
            self.power_ups.append(Shield())

    def update(self, score, game_speed, player):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                player.shield = True
                player.has_power_up = True
                player.type = power_up.type
                player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def clen_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)