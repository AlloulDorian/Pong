import pygame
from pygame.locals import *

class Player:
    def __init__(self,num,wall_dim,wall_coord):
        self.num = num
        self.wall_height, self.wall_width = wall_dim
        self.wall_x, self.wall_y = wall_coord

    def gen_surface(self):
        s = pygame.Surface((self.wall_width,self.wall_height))
        s.fill((255,255,255))
        return s
