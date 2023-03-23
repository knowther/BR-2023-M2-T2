import random
import pygame

from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.clock import Clock
from dino_runner.utils.constants import SHIELD_TYPE, HAMMER_TYPE, CLOCK_TYPE, CLOCK_SOUND
from dino_runner.utils.music_utils import play_sound


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0

        #classe que serve pra controlar quando o poder deve aparecer
    def generate_power_up(self, score):
        power_up_type = [
            Shield(),
            Clock(),
            Hammer(),

        ]
        #se a lista de powerup estiver vazia, ele define quando o powerup vai aparecer +
        #no início da partida essa condição já é atendida e ele já define em que momento do jogo o power_up vai aparecer, quando a condição é atendida+
        # o jogo redefine essa variável para 200/300 acima do que foi definida anteriormente pra sempre ir atualizando o valor de quando o powerup aparece
        if len(self.power_ups) == 0 and self.when_appears == score:
            #aqui escolhe um valor randômico entre 200 e 300 e incrementa no when_appears para o powerup aparecer após atingir essa nova pontuação
            self.when_appears += random.randint(200,300)
            self.power_ups.append(power_up_type[random.randint(0,2)])

    def update(self, score, game, player):
        # if not player.has_power_up:
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
            # se o player colidir com um power up o programa vai:
            if player.dino_rect.colliderect(power_up.rect):
                #conferir o tipo do power up e atribuir as variáveis de acordo com ele
                if power_up.type == SHIELD_TYPE:
                    self.configure_power_up(player, power_up)
                    player.shield = True
                    player.hammer = False
                    player.time_traveling = False
                    player.has_power_up = True
                    self.power_ups.remove(power_up)
                elif power_up.type == HAMMER_TYPE:
                    self.configure_power_up(player, power_up)
                    player.hammer = True
                    player.shield = False
                    player.time_traveling = False
                    player.has_power_up = True
                    self.power_ups.remove(power_up)
                elif power_up.type == CLOCK_TYPE:
                    #o sound tá aqui porque é importante que ele seja tocado quando pega o powerup
                    play_sound(CLOCK_SOUND)
                    self.configure_power_up(player, power_up)
                    player.time_traveling = True
                    player.shield = False
                    player.hammer = False
                    player.has_power_up = True
                    #momento da atribuição do old_game_speed, a variável vai receber o valor do game speed atual, antes de ser acelerada
                    game.old_game_speed = game.game_speed
                    #aqui se incrementa 50 de velocidade, assim seria a "viagem no tempo"
                    game.game_speed += 50
                    self.power_ups.remove(power_up)




    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

#método para abstrair a configuração do power_up
    def configure_power_up(self, player, power_up):
        power_up.start_time = pygame.time.get_ticks()
        player.type = power_up.type
        player.power_up_time = power_up.start_time + (power_up.duration * 1000)


    def clen_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(100, 200)