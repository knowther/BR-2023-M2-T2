import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, CLOCK, SHIELD, \
    HAMMER, SCORE_SOUND, DINO_DEAD, DINO_START, GAME_OVER, CLOUD
from dino_runner.components.dinossaur import Dinosaur
from dino_runner.components.obstacles.obstacleManager import ObstacleManager
from dino_runner.utils.music_utils import play_sound
from dino_runner.utils.text_utils import draw_message_component
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_is_running = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.death_count = 0
        self.high_score = 0
        #variável definida pra receber o gamespeed antes de pegar o power_up
        self.old_game_speed = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()


        # método que controla o estado do jogo, se o jogo está rodando mas não sendo jogado, o menu vai aparecer
    def execute(self):
        self.game_is_running = True
        while self.game_is_running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        #adicionado
        self.reset_game()
        while self.playing:
            self.events()
            self.update()
            self.draw()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.game_is_running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.key_pressed = user_input
        self.player.update()
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score, self, self.player)

    #a cada 30 frames que se passa no jogo, ganhamos 1 ponto
    def update_score(self):
        self.score += 1
        #adicionado
        self.should_increase_speed()

    #verifica se a velocidade deve ser incrementada
    def should_increase_speed(self):
        if self.score % 100 == 0:
            self.game_speed += 2
            play_sound(SCORE_SOUND)



    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(CLOUD, (self.x_pos_bg + image_width, self.y_pos_bg - 300))
        self.screen.blit(CLOUD, (self.x_pos_bg + 1700, self.y_pos_bg - 150))
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:

            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        draw_message_component(
            f"S: {self.score}", self.screen, pos_x_center= 1000, pos_y_center=50
        )
        draw_message_component(
            f"G. speed: {self.game_speed}", self.screen, pos_x_center=150, pos_y_center=50
        )
        if self.high_score > 0:
            draw_message_component(
                f"HI: {self.high_score}", self.screen, pos_x_center= 850, pos_y_center= 50
            )

        pygame.display.update()

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message_component(f'{self.player.type.capitalize()} enabled for {time_to_show} seconds', self.screen, pos_x_center= 550, pos_y_center= 80)
                if self.player.shield:
                    self.screen.blit(SHIELD, ((SCREEN_WIDTH // 2) - (-450), (SCREEN_HEIGHT // 2) - 240))
                elif self.player.hammer:
                    self.screen.blit(HAMMER, ((SCREEN_WIDTH // 2) - (-450), (SCREEN_HEIGHT // 2) - 240))
                else:
                    self.screen.blit(CLOCK, ((SCREEN_WIDTH // 2) - (-450), (SCREEN_HEIGHT // 2) - 240))

                #ponto de balanceamento: se a gamespeed fosse as mesmas 50 durante o efeito do power_up, iria ficar difícil pra o jogador não morrer quando
                #acabasse pois estava muito rápido e acontecia do powerup acabar e você acabar batendo em um obstáculo.
                #para contornar isso fiz o seguinte, atribui a velocidade antes de pegar o relógio pra uma varíavel chamada old_game_speed
                #e então a cada segundo ela vai decrementando o gamespeed atual até o velocidade atual ser menor que a antiga
                #fazendo um efeito de aceleração imediata mas depois decaindo.
                if self.player.time_traveling and self.game_speed > self.old_game_speed:
                    self.game_speed -= 1
            else:
                self.player.shield = False
                self.player.hammer = False
                self.player.time_traveling = False
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.game_is_running = False
            elif event.type == pygame.KEYDOWN:
                self.run()
    def show_menu(self):
        #aqui preenche a tela de braco
        self.screen.fill((255,255,255))
        #desenha o background na tela
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        #desenha o player na tela
        self.player.draw(self.screen)
        #define a imagem do player
        self.player.image = DINO_START
        if self.death_count == 0:
            draw_message_component('Press any key to start', self.screen)
        else:
            if self.score > self.high_score:
                self.high_score = self.score

                #game over adicionado aqui
            self.player.image = DINO_DEAD
            self.screen.blit(GAME_OVER , (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))
            draw_message_component(f'High Score: {self.high_score}', self.screen, pos_y_center= (SCREEN_HEIGHT // 2) - 180)
            draw_message_component(f'You died {self.death_count} times and scored {self.score}', self.screen, pos_y_center= 350)
            # self.create_text('Press any key to start',  (SCREEN_WIDTH // 2) - 40, (SCREEN_HEIGHT // 2) -40)
        pygame.display.update()
        self.handle_events_on_menu()


        #adicionado
    def reset_game(self):
        self.playing = True
        self.obstacle_manager.clean_obstacles()
        self.score = 0
        self.game_speed = 20
        self.power_up_manager.clen_power_ups()