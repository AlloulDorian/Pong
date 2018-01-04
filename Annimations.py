from time import sleep
from sys import exit

class Annimations:
    def __init__(self,pygame,background,screen,dimentions):
        self.pygame=pygame
        self.background=background
        self.screen=screen
        self.height,self.width=dimentions

    def create_text_surface(self,text,color,size):
        myfont = self.pygame.font.SysFont('Comic Sans MS', size)
        textsurface = myfont.render(text, True, color)
        return textsurface

    def menu(self):
        white = (255,255,255)
        grey = (120,120,120)
        i=0
        coef=1
        while True:
            for event in self.pygame.event.get():
                if event.type==self.pygame.KEYDOWN:
                    if event.key==self.pygame.K_SPACE:
                        self.background.fill((0,0,0))
                        self.screen.blit(self.background,(0,0))
                        self.pygame.display.update()
                        textsurface = self.create_text_surface('PONG GAME',white,30)
                        enter_surface = self.create_text_surface('Waiting for players...',grey,20)
                        self.background.blit(textsurface,(self.width/2-90,self.height/5))
                        self.background.blit(enter_surface,(self.width/2-100,self.height/5+100))
                        self.screen.blit(self.background,(0,0))
                        self.pygame.display.update()

                        return
                    elif event.key==self.pygame.K_ESCAPE:
                        return 'QUIT'
            if i>120:
                coef=-1
            if i<30:
                coef=1
            i = i+coef
            sleep(0.01)
            self.background.fill((0,0,0))
            color = (i,i,i)
            textsurface = self.create_text_surface('PONG GAME',white,30)
            enter_surface = self.create_text_surface('Press SPACE to start',color,20)
            or_surface = self.create_text_surface('OR',grey,20)
            exit_surface = self.create_text_surface('Press ESC to escape Pong',color,20)
            self.background.blit(textsurface,(self.width/2-90,self.height/5))
            self.background.blit(enter_surface,(self.width/2-150,self.height/5+100))
            self.background.blit(or_surface,(self.width/2-150,self.height/5+120))
            self.background.blit(exit_surface,(self.width/2-150,self.height/5+140))
            self.screen.blit(self.background,(0,0))
            self.pygame.display.update()
    def display_looser(self,looser):
       white = (255,255,255)
       self.background.fill((0,0,0))
       textsurface = self.create_text_surface('LOOSER: '+looser,white,30)
       self.background.blit(textsurface,(self.width/2-90,self.height/5))
       self.screen.blit(self.background,(0,0))
       self.pygame.display.update()
       sleep(5)
