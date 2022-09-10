import sys
import pygame,os
import random
import time
from pygame.locals import *

class fallobject():
        def __init__(self,p,b,h,c,yv):
                self.x=p[0]
                self.y=p[1]
                self.b=b
                self.h=h
                self.c=c
                self.yv=yv
        def speed(self,r,x):
                self.y+=self.yv
                score=0
                if(self.y<-self.h):
                        score=1
                        self.boxchang(r,x)
                return score
        def boxchang(self,r,x):
                self.h=random.randrange((r*2)+1,(r*3))
                self.b=int((self.h/5)*8)
                self.y=h+self.h
                if(self.yv>fallobjmaxvel):
                        self.yv-=(-1*self.yv)*(fallobjaccper/100)
                self.x=random.randrange(max(0,int(x)-offset),min(int(w)-int(self.b),int(x)+offset))#(0,w-self.b)
                r=random.randrange(200)
                g=random.randrange(200)
                b=random.randrange(200)
                self.c=(r,g,b)
        def display(self):
                pygame.draw.rect(surface,(0,0,0),(self.x,self.y,self.b,self.h))
                r=int((min(self.b-(2*fallboxbor),self.h-(2*fallboxbor))*40/100))
                pygame.draw.rect(surface,self.c,(self.x+fallboxbor,self.y+fallboxbor,self.b-(2*fallboxbor),self.h-(2*fallboxbor)),border_radius=r)
                
class player():
        def __init__(self,p,s,c,h,yv,score):
                self.x=p[0]
                self.y=p[1]
                self.s=s
                self.c=c
                self.yv=yv
                self.h=h
                self.res=False
                self.score=score
        def speed(self):
                self.y+=self.yv
                if(self.y<=h-self.s-(h-li[0][1]) or self.y>=self.s):
                        if(self.yv<=self.s):
                                self.yv+=gravity
                if(self.y>=h-self.s-(h-li[0][1])):
                        self.res=True
        def sco(self,s):
                self.score+=s
        def display(self):
                pygame.draw.circle(surface,(0,0,0),(self.x,self.y),self.s)
                pygame.draw.circle(surface,tuple(self.c),(self.x,self.y),self.s-ballbor)
def start():
        star=True
        surface.fill((124,109,71))
        fot=55
        tt('Press any Key to PLAY',fot,(0,255,100),[0.5,0.5])
        pygame.display.update()
        while star :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        quit()
                if event.type==pygame.KEYDOWN:
                        star=False
            pygame.display.update()

def linepro(rect,cir):
        x,y,b,h=rect
        if abs((x+(b/2))-cir[0])>(cir[2]+(b/2)):
                return False
        elif abs((y+(h/2))-cir[1])>(cir[2]+(h/2)):
                return False
        else:
                return True
        

def tt(txt,s,c,p):
        font = pygame.font.Font('freesansbold.ttf',s)
        text = font.render(txt,True,c)
        textRect = text.get_rect()
        if(p[0]<0.5):
                p[0]=int(p[0]*w+(textRect.w/2))+5
        elif(p[0]>0.5):
                p[0]=int(p[0]*w-(textRect.w/2))-5
        else:
                p[0]=int(w/2)
        p[1]=int(p[1]*h+(textRect.h/2))+5
        textRect.center = (p[0],p[1])
        surface.blit(text, textRect)
        
os.environ['SDL_VIDEO_CENTERED'] = '1' 
pygame.init()
info = pygame.display.Info()
w,h= info.current_w-100,info.current_h-100
surface = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()



li=((int(w/100),int(99*h/100)),(int(99*w/100),int(99*h/100)))
b=20
fb,fh=100,80
fondsize=35
fallobvel=-5
ballxmovvel=10
gravity=0.9
fallobjaccper=5
fallobjmaxvel=-15
ballupvelclick=-20
fallboxbor=5
ballbor=5
hardness=0.5#0-1
offset=int((b*30)*hardness)

def restart():
    start()
    ball=player([w/2,b+1],b,(171, 90, 232),5,0,0)
    fall=fallobject([(w/2),h+500],fb,fh,(0,0,0),fallobvel)
    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if event.type==pygame.KEYDOWN:
                        if(event.key == pygame.K_UP):
                                if(ball.y>ball.s):
                                        ball.yv=ballupvelclick
            keys=pygame.key.get_pressed()
            if(keys[pygame.K_RIGHT] and ball.x+ball.s<w):
                        ball.x+=ballxmovvel
            if(keys[pygame.K_LEFT] and ball.x-ball.s>0):
                        ball.x-=ballxmovvel
            surface.fill((90, 171, 232))
            ball.speed()
            ball.h-=(fall.speed(ball.s,ball.x))
            if(linepro((fall.x,fall.y,fall.b,fall.h),(ball.x,ball.y,ball.s))):
                #ball.score+=100
                ball.sco(100)
                fall.boxchang(ball.s,ball.x)
            fall.display()
            ball.display()
            pygame.draw.line(surface,(189,74,74),li[0],li[1],5)
            tt('Score : {}'.format(ball.score),fondsize,(0,0,0),[0,0])
            tt('Health : {}'.format(ball.h),fondsize,(250,0,0),[1,0])
            pygame.display.update()
            if(ball.h<=0):
                time.sleep(0.5)
                restart()
            if(ball.res==True):
                time.sleep(0.5)
                restart()
            clock.tick(60)
restart()
