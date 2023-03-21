from dino_runner.utils.constants import BIRD
from dino_runner.components.obstacles.obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self):
        super().__init__(BIRD, 0)
        self.rect.y = 250
        self.fly_index = 0


    def draw(self, screen):
        #esse método aqui pega usa o índice do fly que é a iteração a cada frame e divide por 5, até o passo 5 o resoltado do operador // vao ser igual a 0 após 5 vai ser 1 e ao chegar 10 que é 2 ele já reseta o index novamente
        screen.blit(self.image[self.fly_index // 5], self.rect)
        self.fly_index += 1

        if self.step_index >= 10:
            self.fly_index = 0

