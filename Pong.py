#!/usr/bin/env python2.7
import sys
from random import randint, choice
import pygame
from pygame.locals import *

from Ball import Ball
from Player import Player

pygame.font.init()

class Pong:

    def __init__(self,window_size,nb_players=4):
        self.width,self.height = window_size
        self.nb_players = nb_players
        self.ball = Ball(10,(self.width/2,self.height/2)) 
        
        # Fill background
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))

        #Define Ball s orientation
        allowed_values = list(range(-5, 5+1))
        allowed_values.remove(-1)
        allowed_values.remove(0)
        allowed_values.remove(1)
        # can be anything in {-5, ..., 5} \ {-1,0,1}:
        self.coef_y = choice(allowed_values) 
        self.coef_x = -1#[-1,1][randint(0,1)]

        self.ball_tracked = True
        
        # Define players
        wall_player1_2_height = int(round(self.height/6))
        wall_player3_4_width = int(round(self.width/6))
        self.p1 = Player(1,(wall_player1_2_height,10),(0,self.height/2))
        self.p2 = Player(2,(wall_player1_2_height,10),(self.width-10,self.height/2))
        if self.nb_players>=3:
            self.p3 = Player(3,(10,wall_player3_4_width),(self.width/2,0))
        if self.nb_players==4:
            self.p4 = Player(4,(10,wall_player3_4_width),(self.width/2,self.height-10))


    def draw(self):

        # Display ball
        ball_s = self.ball.gen_surface()
        ball_pos = (self.ball.x, self.ball.y)
        self.background.fill((0, 0, 0))
        self.background.blit(ball_s, ball_pos)
        
        # Display Players Walls
        wall_p1 = self.p1.gen_surface()
        self.background.blit(wall_p1, (self.p1.wall_x,self.p1.wall_y))

        wall_p2 = self.p2.gen_surface()
        self.background.blit(wall_p2, (self.p2.wall_x,self.p2.wall_y))

        if self.nb_players==3 or self.nb_players==4:
            wall_p3 = self.p3.gen_surface()
            self.background.blit(wall_p3, (self.p3.wall_x,self.p3.wall_y))
        
        if self.nb_players==4:
            wall_p4 = self.p4.gen_surface()
            self.background.blit(wall_p4, (self.p4.wall_x,self.p4.wall_y))
        
        # Blit everything to the screen
        self.screen.blit(self.background, (0,0))

        
    def movments_calcul(self):
        # Right Side
        if self.ball.x > (self.width-self.p2.wall_width-(self.ball.d)) and self.coef_x==1:
            if self.ball.y>self.p2.wall_y and self.ball.y<self.p2.wall_y+self.p2.wall_height:
                self.coef_x = self.coef_x*-1
            else:
                print('LOOSER: J2')
                sys.exit(0)
        # Left Side
        elif self.ball.x < self.p1.wall_width:
            if self.ball.y>self.p1.wall_y and self.ball.y<self.p1.wall_y+self.p1.wall_height:
                self.coef_x = self.coef_x*-1
            else:
                print('LOOSER: J1')
                sys.exit(0)
        # Down Side
        elif self.ball.y > (self.height-2-self.ball.d/2) and self.nb_players<4:
            self.coef_y = self.coef_y * (-1)
        elif self.nb_players==4 and self.ball.y>(self.height-self.p4.wall_height-self.ball.d):
            if self.ball.x<self.p3.wall_x or self.ball.x>(self.p3.wall_x+self.p3.wall_width):
                print('LOOSER: J4')
                sys.exit(0)
            else:
                self.coef_y = self.coef_y * (-1)
        # Up Side
        elif self.ball.y<3 and self.nb_players==2:
            self.coef_y = self.coef_y * (-1)
        elif self.nb_players>=3 and self.ball.y<self.p3.wall_height:
            if self.ball.x<self.p3.wall_x or self.ball.x>(self.p3.wall_x+self.p3.wall_width):
                print('LOOSER: J3')
                sys.exit(0)
            else:
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
        white = (255,255,255)
        if self.nb_players==2:
            pygame.draw.rect(self.screen,white,(0,0,self.width,2))
            pygame.draw.rect(self.screen,white,(0,self.height-2,self.width,self.height))

        if self.nb_players==3:
            pygame.draw.rect(self.screen,white,(0,self.height-2,self.width,self.height))
        
    def run(self):
        # Initialise screen
        pygame.init()
        pygame.display.set_caption('Pong Game')


        # Event loop
        while 1:
            i = 1
            for event in pygame.event.get():
                if event.type==QUIT or event.key==K_ESCAPE:
                    return
                if event.type == KEYDOWN:
                    if event.key == K_UP and self.p1.wall_y>self.p1.wall_height:
                        self.p1.wall_y = self.p1.wall_y-self.p1.wall_height
                    elif event.key == K_DOWN and self.p1.wall_y<self.height-self.p1.wall_height*2:
                        self.p1.wall_y = self.p1.wall_y+self.p1.wall_height
            # Pseudo IA
            self.p2.wall_y = self.ball.y - self.p2.wall_height/2
            if self.nb_players>=3:
                self.p3.wall_x = self.ball.x - self.p3.wall_width/2
            if self.nb_players==4:
                self.p4.wall_x = self.ball.x - self.p4.wall_width/2

            self.draw()
            self.movments_calcul()
            self.draw_wall()
            pygame.display.update()
            if (self.width>900 and self.width<=1400):
                self.ball.y+=self.coef_y
                self.ball.x+=self.coef_x
            if (self.width>1400):
                self.ball.y+=2*self.coef_y
                self.ball.x+=2*self.coef_x
            if self.width<600:
                pygame.time.wait(int(round(self.width/100))*abs(self.coef_y))

game = Pong((1400,1000))
#game = Pong((300,300))
game.run()
