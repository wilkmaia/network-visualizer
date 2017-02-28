import pygame
import math

import main


class Neuron:
    COLOR = (255, 255, 255)  # White

    def __init__(self, id_, pos_):
        self.pos = pos_
        self.id = id_
        self.radius = math.floor(main.STEP/2)
        self.available = True

    def draw(self, surface):
        if self.available:
            pygame.draw.circle(surface, self.COLOR, self.pos, self.radius)
