import pygame
from pygame.locals import *


class Ball:
    def __init__(self,d,ball_pos = (0,0)):
        self.d = d
        self.x, self.y = ball_pos

    def gen_surface(self):
        d = self.d
        bg = pygame.Surface((d,d))
        bg.fill((0, 0, 0))
        
        circle_c = (255,255,255)
        pygame.draw.circle(bg,circle_c,(d/2,d/2),d/2)

        return bg
