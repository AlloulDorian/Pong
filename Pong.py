#!/usr/bin/env python2.7
import sys
from random import randint
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
        # Fill background
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        self.coef_y = randint(-10,10)
        self.coef_x = [-1,1][randint(0,1)]
        self.ball_tracked = True

    def draw(self):

        # Display ball
        ball_s = self.ball.gen_surface()
        ball_pos = (self.ball.x, self.ball.y)
        self.background.fill((0, 0, 0))
        self.background.blit(ball_s, ball_pos)

        # Blit everything to the screen
        self.screen.blit(self.background, (0,0))
        
    def movments_calcul(self):
        if self.ball.x > (self.width-(self.ball.d)):
            if self.ball_tracked == True:
                self.coef_x = self.coef_x*-1
            else:
                print('WINNER: J1')
                sys.exit(0)
        elif self.ball.x < 1:
            if self.ball_tracked == True:
                self.coef_x = self.coef_x*-1
            else:
                print('WINNER: J2')
                sys.exit(0)
            
        elif self.ball.y > (self.height-2-self.ball.d/2):
            self.coef_y = self.coef_y * (-1)
        elif self.ball.y<3:
            self.coef_y = self.coef_y * (-1)
            
        self.ball.x = self.ball.x+self.coef_x
        self.ball.y = self.ball.y+self.coef_y

    def is_on_wall(self,pos):
        x,y = pos
        x = self.ball.x
        y = self.ball.y

        if self.nb_players == 2:
            if y<3 or y>self.height-3 :
                return True 
            else : 
                return False
        
    def draw_wall(self):
        if self.nb_players == 2:
            white = (255,255,255)
            pygame.draw.rect(self.screen,white,(0,0,self.width,2))
            pygame.draw.rect(self.screen,white,(0,self.height-2,self.width,self.height))

    def run(self):
        # Initialise screen
        pygame.init()
        pygame.display.set_caption('Pong')

        # Event loop
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            self.draw()
            self.movments_calcul()
            self.draw_wall()
            pygame.display.update()
            pygame.time.wait(10)

game = Pong((500,500))
game.run()
