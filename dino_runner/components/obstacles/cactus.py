import random

from dino_runner.components.obstacles.obstacle import Obstacle


class Cactus(Obstacle):
    def __init__(self, image):
<<<<<<< HEAD
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
=======
            self.type = random.randint(0, 2)
            super().__init__(image, self.type)
            self.rect.y = 325 if self.image == SMALL_CACTUS else 300
>>>>>>> adab659 (aula 3 sincrona)
