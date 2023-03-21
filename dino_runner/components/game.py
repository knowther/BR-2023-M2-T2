import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE
from dino_runner.components.dinossaur import Dinosaur
from dino_runner.components.obstacles.obstacleManager import ObstacleManager


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
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.death_count = 0
        self.biggest_score = 0

        # método que controla o estado do jogo, se o jogo está rodando mas não sendo jogado, o menu vai aparecer
    def execute(self):
        self.game_is_running = True
        while self.game_is_running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
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
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()

    #a cada 30 frames que se passa no jogo, ganhamos 1 ponto
    def update_score(self):
        self.score += 1
        self.should_increase_speed()

    #verifica se a velocidade deve ser incrementada
    def should_increase_speed(self):
        if self.score % 100 == 0:
            self.game_speed += 5

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(f"Score: {self.score}", True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        self.screen.blit(text, text_rect)

        pygame.display.update()
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.game_is_running = False
            elif event.type == pygame.KEYDOWN:
                self.run()
    def show_menu(self):
        self.screen.fill((255,255,255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            self.create_text('Press any key to start', half_screen_width, half_screen_height)
        else:
            if self.score > self.biggest_score:
                self.biggest_score = self.score
            self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))
            self.create_text(f'High Score: {self.biggest_score}', half_screen_width, half_screen_height - 180)
            self.create_text(f'You death {self.death_count} times and scored {self.score}', half_screen_width, half_screen_height)
            self.create_text('Press any key to start',  half_screen_width, half_screen_height + 30)
        pygame.display.update()
        self.handle_events_on_menu()

    def create_text(self, text_to_render, pos1, pos2):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(text_to_render, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (pos1, pos2)
        self.screen.blit(text, text_rect)
    def reset_game(self):
        self.playing = True
        self.obstacle_manager.clean_obstacles()
        self.score = 0
        self.game_speed = 20