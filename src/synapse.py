import pygame
import math
import random


class Synapse:
    def __init__(self, id_, src, dst, w, c=(255, 0, 0)):
        self.startPos = src.pos
        self.endPos = dst.pos
        self.src = src
        self.dst = dst
        self.id = id_
        self.w = w
        self.COLOR = c
        self.available = True
        self.c = [(125, 125, 0), (0, 125, 125), (125, 0, 125), (200, 100, 100),
                  (150, 175, 50), (255, 100, 0), (0, 255, 100), (235, 200, 100)]

    def draw(self, surface):
        if self.available:
            if self.COLOR == (0, 0, 100):
                self.COLOR = random.choice(self.c)
                self.c.remove(self.COLOR)
            pygame.draw.line(surface, self.COLOR, self.startPos, self.endPos, 3)
            pygame.draw.circle(surface, self.COLOR, self.startPos, 5)
            y2 = self.endPos[1]
            y1 = self.startPos[1]
            x2 = self.endPos[0]
            x1 = self.startPos[0]

            m = (y2 - y1) / (x2 - x1 + 0.000001)
            alpha1 = math.atan(m)

            m1 = - math.cos(alpha1 + math.pi/4 + math.pi/256)\
                 / math.sin(alpha1 + math.pi/4 + math.pi/256)
            m2 = math.tan(alpha1+math.pi/4)
            d = 15

            n = 1
            nn = 1
            if x1 == x2:
                n = 2
                if y1 > y2:
                    nn = 2
                    n = 1
            _x1 = x2 + math.pow(-1, nn) * d / math.sqrt(m1 * m1 + 1)
            _x2 = x2 + math.pow(-1, n) * d / math.sqrt(m2 * m2 + 1)

            _y1 = m1 * (_x1 - x2) + y2
            _y2 = m2 * (_x2 - x2) + y2

            p1 = (_x1, _y1)
            p2 = (_x2, _y2)
            pygame.draw.line(surface, self.COLOR, p1, self.endPos, 3)
            pygame.draw.line(surface, self.COLOR, p2, self.endPos, 3)
