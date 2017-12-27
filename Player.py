import pygame
from pygame.locals import *

class Player:
    def __init__(self,num,name,wall_dim,wall_y):
        self.num = num
        self.name = name
        self.wall_height, self.wall_width = wall_dim
        self.wall_y = wall_y

    def gen_surface(self):
        s = pygame.Surface((10,self.wall_height))
        s.fill((255,255,255))
        return s
