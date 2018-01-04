#!/usr/bin/env python2.7
import sys
from time import sleep
from random import randint, choice
import pygame
from pygame.locals import *

from Ball import Ball
from Player import Player
from Networking import Networking
from Annimations import Annimations

pygame.font.init()

icon_32x32 = pygame.image.load("image/ping.png")
pygame.display.set_icon(icon_32x32)

class Pong:

    def __init__(self,window_size,nb_players=2):
        # Arguments verifications
        if len(sys.argv[1:])<4 and len(sys.argv[1:])>1 and sys.argv[1]=="server" :
            print('4 arguments needed: example: \n./Pong.py "server "127.0.0.1" 4444 2')
            sys.exit(1)
        if len(sys.argv[1:])<3:
            print('Usage:\t./Pong.py <mode> <ip_address> <nb_port> <nb_players>\
                    \n\n\t- mode:\t\tCan be "server" or "client"\
                    \n\t- ip_address:\tCan be localhost (127.0.0.1)\
                    \n\t- nb_port:\tSpecify an available port like maybe 4444\
                    \n\t- nb_players:\tJust needed for the "server" mode\
                    \n')
            sys.exit(1)
        # Import Arguments
        self.mode = str(sys.argv[1])
        self.ip_address = str(sys.argv[2])
        self.port = int(sys.argv[3])
        if self.mode=='server':
            self.nb_players = int(sys.argv[4])
        self.IA=''
        if len(sys.argv[1:])==5:
            self.IA=sys.argv[5]


        self.width,self.height = window_size
        self.ball = Ball(10,(self.width/2,self.height/2)) 
        
        # Fill background
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))

        self.annim = Annimations(pygame,self.background,self.screen,(self.height,self.width))
        
        #Define Ball s orientation
        allowed_values = list(range(-5, 5+1))
        allowed_values.remove(-1)
        allowed_values.remove(0)
        allowed_values.remove(1)
        # can be anything in {-5, ..., 5} \ {-1,0,1}:
        self.coef_y = -1#choice(allowed_values) 
        self.coef_x = [-1,1][randint(0,1)]

        self.ball_tracked = True
        
        # Define players
        wall_player1_2_height = int(round(self.height/6))
        wall_player3_4_width = int(round(self.width/6))
        self.L_players = []
        self.p1 = Player(1,(wall_player1_2_height,10),(0,self.height/2))
        self.p2 = Player(2,(wall_player1_2_height,10),(self.width-10,self.height/2))
        self.L_players.append(self.p1)
        self.L_players.append(self.p2)
        if self.mode=='server':
            if self.nb_players>=3:
                self.p3 = Player(3,(10,wall_player3_4_width),(self.width/2,0))
                self.L_players.append(self.p3)
            if self.nb_players==4:
                self.p4 = Player(4,(10,wall_player3_4_width),(self.width/2,self.height-10))
                self.L_players.append(self.p4)


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
                self.annim.display_looser('J2')
                if self.mode=='server':
                    for sock in self.network.L_sockets:
                        sock.close()
                else:
                    self.network.host_socket.close()
                #sys.exit(0)
                return 'replay'
        # Left Side
        elif self.ball.x < self.p1.wall_width:
            if self.ball.y>self.p1.wall_y and self.ball.y<self.p1.wall_y+self.p1.wall_height:
                self.coef_x = self.coef_x*-1
            else:
                print('LOOSER: J1')
                self.annim.display_looser('J1')
                if self.mode=='server':
                    for sock in self.network.L_sockets:
                        sock.close()
                else:
                    self.network.host_socket.close()
                #sys.exit(0)
                return 'replay'
        # Down Side
        elif self.ball.y > (self.height-2-self.ball.d/2) and self.nb_players<4:
            self.coef_y = self.coef_y * (-1)
        elif self.nb_players==4 and self.ball.y>(self.height-self.p4.wall_height-self.ball.d):
            if self.ball.x<self.p3.wall_x or self.ball.x>(self.p3.wall_x+self.p3.wall_width):
                print('LOOSER: J4')
                self.annim.display_looser('J4')
                if self.mode=='server':
                    for sock in self.network.L_sockets:
                        sock.close()
                else:
                    self.network.host_socket.close()
                #sys.exit(0)
                return 'replay'
            else:
                self.coef_y = self.coef_y * (-1)
        # Up Side
        elif self.ball.y<3 and self.nb_players==2:
            self.coef_y = self.coef_y * (-1)
        elif self.nb_players>=3 and self.ball.y<self.p3.wall_height:
            if self.ball.x<self.p3.wall_x or self.ball.x>(self.p3.wall_x+self.p3.wall_width):
                print('LOOSER: J3')
                self.annim.display_looser('J2')
                if self.mode=='server':
                    for sock in self.network.L_sockets:
                        sock.close()
                else:
                    self.network.host_socket.close()
                #sys.exit(0)
                return 'replay'
            else:
                self.coef_y = self.coef_y * (-1)
            
        self.ball.x = self.ball.x+self.coef_x
        self.ball.y = self.ball.y+self.coef_y
        return 'ok'
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


        ret = self.annim.menu()
        if ret=='QUIT':
            return 'QUIT'
        
        if self.mode=='server':
            self.network = Networking(self.ip_address,self.port,self.nb_players-1)
            self.network.run_server_side((self.coef_x,self.coef_y))
            if self.nb_players>=2:
                self.p2.socket = self.network.L_sockets[0]
            if self.nb_players>=3:
                self.p3.socket = self.network.L_sockets[1]
            if self.nb_players==4:
                self.p4.socket = self.network.L_sockets[2]

                
        else:
            self.network = Networking(self.ip_address,self.port,0)
            self.network.run_client_side()
            self.coef_x = self.network.coef_x
            self.coef_y = self.network.coef_y
            self.nb_players= self.network.nb_players
            if self.nb_players>=3:
                self.p3 = Player(3,(10,wall_player3_4_width),(self.width/2,0))
                self.L_players.append(self.p3)
            if self.nb_players==4:
                self.p4 = Player(4,(10,wall_player3_4_width),(self.width/2,self.height-10))
                self.L_players.append(self.p4)


        # Event loop
        while 1:
            if self.mode=='server':
                msg = self.network.server_detect_if_client_sent_message()
                if msg.split(':')[-1]!='':
                    player,mov = (int(msg.split(':')[-2]),msg.split(':')[-1])
                    print('player:'+str(player)+'\tmov:'+mov)
                    if mov=='K_UP' and self.L_players[player-1].wall_y>self.L_players[player-1].wall_height:
                        self.network.server_broadcast_message(player,'K_UP')
                        if player==2:
                            self.p2.wall_y = self.p2.wall_y-self.p2.wall_height
                    elif mov=='K_DOWN' and self.L_players[player-1].wall_y<self.height-self.L_players[player-1].wall_height*2:
                        self.network.server_broadcast_message(player,'K_DOWN')

                        if player==2:
                            self.p2.wall_y = self.p2.wall_y+self.L_players[player-1].wall_height
                    elif mov=='K_RIGHT' and self.L_players[player-1].wall_x<self.width-self.L_players[player-1].wall_width*2:
                        self.network.server_broadcast_message(player,'K_RIGHT')
                        print('cense etre p3 right'+str(player))
                        if player==3:
                            self.p3.wall_x = self.p3.wall_x+self.p3.wall_width
                        if player==4:
                            self.p4.wall_x = self.p4.wall_x+self.p4.wall_width
                    elif mov=='K_LEFT' and self.L_players[player-1].wall_x>self.L_players[player-1].wall_width:
                        self.network.server_broadcast_message(player,'K_LEFT')
                        print('cense etre p3 left'+str(player))
                        if player==3:
                            self.p3.wall_x = self.p3.wall_x-self.p3.wall_width
                        if player==4:
                            self.p4.wall_x = self.p4.wall_x-self.p4.wall_width
            # If mode == client
            else:
                msg=''
                msg = self.network.client_detect_if_server_sent_message()
                if msg.split(':')[-1]!='' and  msg.split(':')[-2]!='' and msg.split(':')[-2]!='K_LEFT2' and msg.split(':')[-2]!='K_RIGHT2': 
                    player,mov = (int(msg.split(':')[-2]),msg.split(':')[-1])
                    print('player:'+str(player)+'\tmov:'+mov+'\tmov:'+mov)
                    if mov=='K_UP' and self.L_players[self.network.num_player-2].wall_y>self.L_players[self.network.num_player-2].wall_height:
                        self.L_players[self.network.num_player-2].wall_y = self.L_players[self.network.num_player-2].wall_y-self.L_players[self.network.num_player-2].wall_height
                    elif mov=='K_DOWN' and self.L_players[self.network.num_player-2].wall_y<self.height-self.L_players[self.network.num_player-2].wall_height*2:
                        self.L_players[self.network.num_player-2].wall_y = self.L_players[self.network.num_player-2].wall_y+self.L_players[self.network.num_player-2].wall_height
                    elif mov=='K_RIGHT' and self.L_players[player-1].wall_x<self.width-self.L_players[player-1].wall_width*2:
                        print(str(player))
                        if player==3:
                            
                            self.p3.wall_x = self.p3.wall_x+self.p3.wall_width
                        if player==4:
                            self.p4.wall_x = self.p4.wall_x+self.p4.wall_width
                    elif mov=='K_LEFT' and self.L_players[player-1].wall_x>self.L_players[player-1].wall_width:
                        print(str(player))
                        if player==3:
                
                            self.p3.wall_x = self.p3.wall_x-self.p3.wall_width
                        if player==4:
                            self.p4.wall_x = self.p4.wall_x-self.p4.wall_width

                
            for event in pygame.event.get():
                #if event.type==pygame.QUIT or event.key==K_ESCAPE:
                #    return
                if self.mode=='server':
                    if event.type == KEYDOWN:
                        if event.key == K_UP and self.p1.wall_y>self.p1.wall_height:
                            self.p1.wall_y = self.p1.wall_y-self.p1.wall_height
                            self.network.server_send_data_to_all_players('1'+':'+'K_UP')
                        elif event.key == K_DOWN and self.p1.wall_y<self.height-self.p1.wall_height*2:
                            self.p1.wall_y = self.p1.wall_y+self.p1.wall_height
                            self.network.server_send_data_to_all_players('1'+':'+'K_DOWN')
                # If self.mode!='server'
                else:
                    if event.type == KEYDOWN:
                        if self.network.num_player==2:
                            if event.key == K_UP and self.L_players[self.network.num_player-1].wall_y>self.L_players[self.network.num_player-1].wall_height:
                                self.L_players[self.network.num_player-1].wall_y = self.L_players[self.network.num_player-1].wall_y-self.L_players[self.network.num_player-1].wall_height
                                self.network.client_send_data(str(self.network.num_player)+':'+'K_UP')
                            elif event.key == K_DOWN and self.L_players[self.network.num_player-1].wall_y<self.height-self.L_players[self.network.num_player-1].wall_height*2:
                                self.L_players[self.network.num_player-1].wall_y = self.L_players[self.network.num_player-1].wall_y+self.L_players[self.network.num_player-1].wall_height
                                self.network.client_send_data(str(self.network.num_player)+':'+'K_DOWN')
                        if event.key == K_RIGHT and self.L_players[self.network.num_player-1].wall_x<self.width-self.L_players[self.network.num_player-1].wall_width*2:
                            if(self.network.num_player==3 or self.network.num_player==4):    
                                self.L_players[self.network.num_player-1].wall_x = self.L_players[self.network.num_player-1].wall_x+self.L_players[self.network.num_player-1].wall_width
                                self.network.client_send_data(str(self.network.num_player)+':'+'K_RIGHT')
                        if event.key == K_LEFT and self.L_players[self.network.num_player-1].wall_x>self.L_players[self.network.num_player-1].wall_width:
                            if(self.network.num_player==3 or self.network.num_player==4):    
                                self.L_players[self.network.num_player-1].wall_x = self.L_players[self.network.num_player-1].wall_x+self.L_players[self.network.num_player-1].wall_width
                                self.network.client_send_data(str(self.network.num_player)+':'+'K_RIGHT')



            # IA to test or to have fun lonely
            if sys.argv[1:]==5:
                for letter in self.IA:
                    if letter=='1':
                        self.p1.wall_y = self.ball.y - self.p1.wall_height/2
                    if letter=='2':
                        self.p2.wall_y = self.ball.y - self.p2.wall_height/2
                    if letter=='3':
                        self.p3.wall_x = self.ball.x - self.p3.wall_width/2
                    if letter=='4':
                        self.p4.wall_x = self.ball.x - self.p4.wall_width/2

            self.draw()
            redo = self.movments_calcul()
            if redo=='replay':
                return 'replay'
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

#game = Pong((1400,1000))
ret = ''
while ret!='QUIT':
    game = Pong((700,500))
    ret=game.run()
