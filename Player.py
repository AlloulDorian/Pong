import pygame
from pygame.locals import *

class Player:
    def __init__(self,num,name,wall_long,wall_y):
        self.num = num
        self.name = name
        self.wall_long = wall_long
        self.wall_y = wall_y

    def gen_surface(self):
        s = pygame.Surface((10,self.wall_long))
        s.fill((255,255,255))
        return s
