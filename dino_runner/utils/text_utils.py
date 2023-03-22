import pygame, sys, os

from dino_runner.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH


font = os.path.join("assets", 'PressStart2P-Regular.ttf')


FONT_COLOR = (0,0,0)
FONT_SIZE = 18
#fonte do jogo definida localmente
#esse método aqui pega o caminho do sistema para o projeto e navega entre os diretórios passados como parâmetro
FONT_STYLE = os.path.join("dino_runner", "assets", 'PressStart2P-Regular.ttf')


def draw_message_component(
        message,
        screen,
        font_color=FONT_COLOR,
        font_size=FONT_SIZE,
        pos_y_center = SCREEN_HEIGHT // 2,
        pos_x_center= SCREEN_WIDTH // 2
):
    font = pygame.font.Font(FONT_STYLE, font_size)
    text = font.render(message, True, font_color)
    text_rect = text.get_rect()
    text_rect.center = (pos_x_center, pos_y_center)
    screen.blit(text, text_rect)