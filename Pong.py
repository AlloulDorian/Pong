#!/usr/bin/env python2.7
import sys
from random import randint, choice
import pygame
from pygame.locals import *

from Ball import Ball
from Player import Player

pygame.font.init()

icon_32x32 = pygame.image.load("ping.png")
pygame.display.set_icon(icon_32x32)

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

        #Define Ball's orientation
        allowed_values = list(range(-5, 5+1))
        allowed_values.remove(-1)
        allowed_values.remove(0)
        allowed_values.remove(1)
        # can be anything in {-5, ..., 5} \ {-1,0,1}:
        self.coef_y = choice(allowed_values) 
        self.coef_x = -1#[-1,1][randint(0,1)]

        self.ball_tracked = True
        self.p1 = Player(1,'toto',(self.height/6,10),self.height/2)
        self.p2 = Player(2,'titi',(self.height/6,10),self.height/2)

    def draw(self):

        # Display ball
        ball_s = self.ball.gen_surface()
        ball_pos = (self.ball.x, self.ball.y)
        self.background.fill((0, 0, 0))
        self.background.blit(ball_s, ball_pos)
        
        # Display Player Walls
        wall_p1 = self.p1.gen_surface()
        self.background.blit(wall_p1, (0,self.p1.wall_y))

        wall_p2 = self.p2.gen_surface()
        self.background.blit(wall_p2, (self.width-10,self.p2.wall_y))

        # Blit everything to the screen
        self.screen.blit(self.background, (0,0))

        
    def movments_calcul(self):
        if self.ball.x > (self.width-self.p2.wall_width-(self.ball.d)) and self.coef_x==1:
            if self.ball.y>self.p2.wall_y and self.ball.y<self.p2.wall_y+self.p2.wall_height:
                self.coef_x = self.coef_x*-1
            else:
                print('WINNER: J1')
                sys.exit(0)
        elif self.ball.x < self.p1.wall_width:
            if self.ball.y>self.p1.wall_y and self.ball.y<self.p1.wall_y+self.p1.wall_height:
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
                if event.type == KEYDOWN:
                    if event.key == K_UP and self.p1.wall_y>self.p1.wall_height:
                        self.p1.wall_y = self.p1.wall_y-self.p1.wall_height
                    elif event.key == K_DOWN and self.p1.wall_y<self.height-self.p1.wall_height*2:
                        self.p1.wall_y = self.p1.wall_y+self.p1.wall_height
            self.p2.wall_y = self.ball.y - self.p2.wall_y/2
            self.draw()
            self.movments_calcul()
            self.draw_wall()
            pygame.display.update()
            pygame.time.wait(2*abs(self.coef_y))

game = Pong((500,500))
game.run()
