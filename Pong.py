#!/usr/bin/env python2.7
import pygame
from pygame.locals import *

from Ball import Ball
from Player import Player

pygame.font.init()

class Pong:

    def __init__(self,window_size,nb_players=2):
        self.width,self.height = window_size
        self.nb_players = nb_players
        self.ball = Ball(10,(self.width/2,self.height/2)) 

    def draw(self,canvas,L_obj):
        return


    def run(self):
        # Initialise screen
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Pong')

        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))

        # Display ball
        ball_s = self.ball.gen_surface()
        ball_pos = (self.ball.x, self.ball.y)
        background.blit(ball_s, ball_pos)

        # Blit everything to the screen
        screen.blit(background, ball_pos)
        pygame.display.flip()

        # Event loop
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            screen.blit(background, (0, 0))
            pygame.display.flip()

game = Pong((500,500))
game.run()
