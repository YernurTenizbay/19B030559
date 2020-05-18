import pygame
import uuid
import pika
import sys
from threading import Thread
import colorsys
import json
import random
from math import *

pygame.init()
walls2=pygame.image.load('wall2.png')
timeover=pygame.image.load('timeover.png')
moves=pygame.mixer.Sound('moves.wav')
youlose=pygame.image.load('youlose.png')
youwon=pygame.image.load('youwon.png')
Mbullet=pygame.image.load('pula.png')
Mtank=pygame.image.load('Mtank.png')
MEtank=pygame.image.load('MEtank.png')
menuselect2=pygame.mixer.Sound("select2.wav")
wallsound=pygame.mixer.Sound("wall.wav")
foodsound=pygame.mixer.Sound("Fruit.wav")
foodimage=pygame.image.load("Bold.png")
wallimage=pygame.image.load("wall.png")
menuback=pygame.mixer.Sound('menu.wav')
menuselect=pygame.mixer.Sound('select.wav')
gameover=pygame.image.load("gameover.png")
mytank=pygame.image.load('tankbody2.png')
gameover_sound=pygame.mixer.Sound('gameover.wav')
mygun=pygame.image.load("tankb5.png")
oth_tank=pygame.image.load("tankbodyenemy2.png")
oth_gun=pygame.image.load("tankbenemy5.png")
window = pygame.display.set_mode((1000,600))
soundbullet=pygame.mixer.Sound("battle-city-sfx-6.wav")
soundbody=pygame.mixer.Sound("move.wav")
soundrote=pygame.mixer.Sound("rotate.wav")
soundbody.set_volume(0.1)
menuback.set_volume(0.3)
foodsound.set_volume(4)
soundrote.set_volume(0.1)
screen=pygame.image.load("tank.jpg")
Font = pygame.font.SysFont("Times New Roman", 20)
font=pygame.font.Font("18930.ttf", 50)
rad = pi/180

count=1
class Menu():
    
    def __init__(self,items=[120,140,u'item',(250,250,30),(250,30,250),0]):
        self.items=items
        
    def render(self,poverhnost,font,num_item):
        for i in self.items:
            if num_item==i[5]:
                poverhnost.blit(font.render(i[2],1,i[4]),(i[0],i[1]))
            else:
                poverhnost.blit(font.render(i[2],1,i[3]),(i[0],i[1]))
    def menu(self):
        done=True
        font_menu=pygame.font.Font("18930.ttf", 50)
        item=0
        
        while done:
            pygame.mixer.Sound.play(menuback)
            
            mp=pygame.mouse.get_pos()
            for i in self.items:
                if mp[0]>i[0] and mp[0]<i[0]+155 and  mp[1]<i[1]+50 and mp[1]>i[1]:
                    
                    item=i[5]
                
            self.render(screen,font_menu,item)      
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    pygame.mixer.Sound.stop(menuback)
                    sys.exit()
                if e.type==pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pygame.mixer.Sound.stop(menuback)
                        sys.exit()
                    if e.key==pygame.K_UP:
                        if item>0:
                            item-=1
                            pygame.mixer.Sound.play(menuselect2)
                    if e.key==pygame.K_DOWN:
                        if item<len(self.items)-1:
                            item+=1
                            pygame.mixer.Sound.play(menuselect2)
                
                if e.type ==pygame.MOUSEBUTTONDOWN and e.button==1 or e.type == pygame.KEYDOWN and e.key == pygame.K_RSHIFT:
                    
                    if item==0:
                        pygame.mixer.Sound.stop(menuback)
                        pygame.mixer.Sound.play(menuselect)
                        done=False
                        Single_tank()
                       
                        
                    elif item==1:
                        pygame.mixer.Sound.stop(menuback)
                        pygame.mixer.Sound.play(menuselect)
                        done=False
                        Multi_tank()
                        
                    elif item==2:
                        pygame.mixer.Sound.stop(menuback)
                        pygame.mixer.Sound.play(menuselect)
                        done=False
                        Multi_AI()
                                               
                    elif item==3:
                        pygame.mixer.Sound.stop(menuback)
                        pygame.mixer.Sound.play(menuselect)
                        sys.exit()

            
            window.blit(screen,(0,0))
            pygame.display.flip()
def Single_tank():
    class Tank():
        def __init__(self):
            self.tele=2
            self.hp=3
            self.x = 200
            self.y = 200
            self.size = 64
            self.speed = 25
            # һself.body = pygame.Surface((self.size,self.size))
            self.body = mytank
            # self.body.set_colorkey((0,0,0))
            # self.body.fill((0,255,0))
            self.rect = self.body.get_rect()
            self.angle = 0
            self.vel=100
            self.circle = self.body.copy()
            self.circle.set_colorkey((0,255,0))
            self.gun=mygun
            self.gun_r=self.gun.get_rect()
            self.gun_r.center=(0,0)
            self.anglegun=180
            self.direct=True
            self.food_dir=False
            self.keep_move=False
            self.zaderzhka = 0
        def move(self,k,sec):
            
            self.speed=self.vel*sec
            #Keep moving
            if k[pygame.K_n]:
                self.keep_move = True
            elif k[pygame.K_m]:
                self.keep_move = False
            if k[pygame.K_w]:
                self.direct=True               
                if not(self.keep_move):
                    self.x += self.speed * cos(self.angle*rad)
                    self.y -= self.speed * sin(self.angle*rad) 
                if self.x>1000:
                    self.x=0
                elif self.x<0:
                    self.x=800
                if self.y>600:
                    self.y=0
                elif self.y<0:
                    self.y=600
                pygame.mixer.Sound.play(soundbody)
            elif k[pygame.K_s]:
                self.direct=False
                if not(self.keep_move):           
                    self.x -= self.speed * cos(self.angle*rad)
                    self.y += self.speed * sin(self.angle*rad)
                if self.x>1000:
                    self.x=0
                elif self.x<0:
                    self.x=1000
                if self.y>600:
                    self.y=0
                elif self.y<0:
                    self.y=600
                pygame.mixer.Sound.play(soundbody)
            if self.keep_move:
                if self.direct==True:
                    if k[pygame.K_w]:
                        self.vel=self.vel+0
                    self.x+= self.speed * cos(self.angle*rad)
                    self.y -= self.speed * sin(self.angle*rad)
                if self.direct==False:
                    
                    if k[pygame.K_s]:
                        self.vel=self.vel-0
                    self.x -= self.speed * cos(self.angle*rad)
                    self.y += self.speed * sin(self.angle*rad)
                if self.x>1000:
                    self.x=0
                elif self.x<0:
                    self.x=1000
                if self.y>600:
                    self.y=0
                elif self.y<0:
                    self.y=600
            
            if k[pygame.K_SPACE] and (pygame.time.get_ticks() - self.zaderzhka)/1000 >=1:
                    bullets.append(Bullet(self.x,self.y,self.anglegun,"tank1"))
                    pygame.mixer.Sound.play(soundbullet)
                    self.zaderzhka = pygame.time.get_ticks()
                    self.tele=3 
            if self.tele==3 and k[pygame.K_z]: 
                for f in bullets:
                    self.x=f.x
                    self.y=f.y
                    self.tele=2  
            
                

            self.rect.center = (self.x,self.y)
            self.gun_r.center= (self.x-self.size/2,self.y)
            self.collision()
        def rotate(self,k):
            if k[pygame.K_a]:
                self.angle +=1
                self.anglegun+=1
                pygame.mixer.Sound.play(soundbody)
            elif k[pygame.K_d]:
                self.angle -=1
                self.anglegun-=1
                pygame.mixer.Sound.play(soundbody)
            if k[pygame.K_q]:
                self.anglegun +=1
                pygame.mixer.Sound.play(soundrote)
            elif k[pygame.K_e]:
                self.anglegun -=1
                pygame.mixer.Sound.play(soundrote)
            self.angle%=360
            
        def draw(self):
            old_center = self.rect.center
            old_guncenter=self.gun_r.center
            new = pygame.transform.rotate(self.body, self.angle)
            new1=pygame.transform.rotate(self.gun,self.anglegun)
            self.rect = new.get_rect()
            self.gun_r=new1.get_rect()
            self.rect.center = old_center
            self.gun_r.center=old_center
            
            # self.gun_r.center = (old_center[0]+10,old_center[1]+10)ы
            window.blit(new, self.rect)
            window.blit(new1,self.gun_r)
            
            # pygame.draw.circle(self.circle, (0,0,255),(5,5), 5)
            # window.blit(self.circle, (self.x-5,self.y-5)
        def collision(self):
            for f in bullets:
                if self.rect.colliderect(f.rect) and f.boss != "tank1":
                    self.hp-=1
                    bullets.remove(f)
                    
            for w in walls:
                if self.rect.colliderect(w.rect):
                    self.hp-=1
                    pygame.mixer.Sound.play(wallsound)
                    walls.remove(w)
            for g in foods:
                if self.rect.colliderect(g.rect):
                    pygame.mixer.Sound.play(foodsound)
                    self.hp+=1
                    self.vel*=2
                    self.food_dir=True
                    foods.remove(g)

    class Tank2():
        def __init__(self):
            self.x = 400
            self.y = 400
            self.hp=3
            self.size = 64
            self.vel=100
            self.speed = 25
            self.direct=True
            # һself.body = pygame.Surface((self.size,self.size))
            self.body = oth_tank
            # self.body.set_colorkey((0,0,0))
            # self.body.fill((0,255,0))
            self.rect = self.body.get_rect()
            self.angle = 0
            self.circle = self.body.copy()
            self.circle.set_colorkey((0,255,0))
            self.gun=oth_gun
            self.gun_r=self.gun.get_rect()
            self.gun_r.center=(0,0)
            self.anglegun=180
            self.keep_move=False
            self.zaderzhka = 0
        def move(self,k,sec):
            self.speed=self.vel*sec
            #Keep moving
            if k[pygame.K_KP4]:
                self.keep_move = True
            elif k[pygame.K_KP6]:
                self.keep_move = False
            if k[pygame.K_UP]:
                self.direct=True
                if not(self.keep_move):
                    self.x += self.speed * cos(self.angle*rad)
                    self.y -= self.speed * sin(self.angle*rad) 
                if self.x>1000:
                    self.x=0
                elif self.x<0:
                    self.x=1000
                if self.y>600:
                    self.y=0
                elif self.y<0:
                    self.y=600
                pygame.mixer.Sound.play(soundbody)
            elif k[pygame.K_DOWN]:
                self.direct=False
                if not(self.keep_move):           
                    self.x -= self.speed * cos(self.angle*rad)
                    self.y += self.speed * sin(self.angle*rad)
                if self.x>1000:
                    self.x=0
                elif self.x<0:
                    self.x=1000
                if self.y>600:
                    self.y=0
                elif self.y<0:
                    self.y=600
                pygame.mixer.Sound.play(soundbody)
            if self.keep_move:
                if self.direct==True:
                    self.x+= self.speed * cos(self.angle*rad)
                    self.y -= self.speed * sin(self.angle*rad)
                if self.direct==False:
                    self.x -= self.speed * cos(self.angle*rad)
                    self.y += self.speed * sin(self.angle*rad)
                if self.x>1000:
                    self.x=0
                elif self.x<0:
                    self.x=1000
                if self.y>600:
                    self.y=0
                elif self.y<0:
                    self.y=600
            if k[pygame.K_RETURN] and (pygame.time.get_ticks() - self.zaderzhka)/1000 >=1:
                bullets.append(Bullet(tank2.x,tank2.y,tank2.anglegun,"tank2"))
                pygame.mixer.Sound.play(soundbullet)
                self.zaderzhka = pygame.time.get_ticks()
                
            self.rect.center = (self.x,self.y)
            self.gun_r.center= (self.x-self.size/2,self.y)
            self.collision()
        def rotate(self,k):
            if k[pygame.K_LEFT]:
                self.angle +=1
                self.anglegun+=1
                pygame.mixer.Sound.play(soundbody)
                pygame.mixer.music.stop()
            elif k[pygame.K_RIGHT]:
                self.angle -=1
                self.anglegun-=1
                pygame.mixer.Sound.play(soundbody)
                pygame.mixer.music.stop()
            if k[pygame.K_KP1]:
                self.anglegun+=1
                pygame.mixer.Sound.play(soundrote)
                pygame.mixer.music.stop()
            elif k[pygame.K_KP3]:
                self.anglegun-=1
                pygame.mixer.Sound.play(soundrote)
                pygame.mixer.music.stop()
            self.angle%=360
        def draw(self):
            old_center = self.rect.center
            old_guncenter=self.gun_r.center
            new = pygame.transform.rotate(self.body, self.angle)
            new1=pygame.transform.rotate(self.gun,self.anglegun)
            self.rect = new.get_rect()
            self.gun_r=new1.get_rect()
            self.rect.center = old_center
            self.gun_r.center=old_center
            # self.gun_r.center = (old_center[0]+10,old_center[1]+10)ы
            window.blit(new, self.rect)
            window.blit(new1,self.gun_r)
        def collision(self):
            for f in bullets:
                if self.rect.colliderect(f.rect) and f.boss != "tank2":
                    self.hp-=1
                    bullets.remove(f)
            for w in walls:
                if self.rect.colliderect(w.rect):
                    self.hp-=1
                    pygame.mixer.Sound.play(wallsound)
                    walls.remove(w)
            for g in foods:
                if self.rect.colliderect(g.rect):
                    
                    self.hp+=1
                    self.vel*=2
                    self.food_dir=True
                    foods.remove(g)
    class Bullet():
        def __init__(self,x,y,angle,boss):
            
            self.angle = angle
            self.x = x -24*cos(self.angle*rad)
            self.y = y +24*sin(self.angle*rad)
            if tank.food_dir==True:
                pygame.mixer.Sound.play(foodsound)
                self.speed=40
            else:
                self.speed=20
            self.size = 5
            self.boss = boss
            #self.bullet = pygame.Surface((25,25))
            #self.bullet.set_colorkey((0,0,0))
            #self.bullet.fill((255,0,0))
            self.bullet = pygame.image.load("bullet2.png")
            self.rect = self.bullet.get_rect()
            self.remove = 0

        def move(self):
            self.x -=self.speed * cos(self.angle*rad)
            self.y +=self.speed * sin(self.angle*rad)
            if self.x >=1000 or self.y >=600 or self.x<=0 or self.y<=0:
                self.remove = 1
            self.rect.center = (self.x,self.y)
            
                   

        def draw(self):
            old_center = self.rect.center
            new = pygame.transform.rotate(self.bullet, self.angle + 90)
            self.rect = new.get_rect()
            self.rect.center = old_center
            window.blit(new, self.rect)
    
            
            
    class Wall():
        def __init__(self,x,y):
            self.x=x
            self.y=y
            self.walls=wallimage 
            self.walls2=walls2
            self.size=16
            self.hp=2
            self.rect = self.walls.get_rect()
            self.rect.center = (self.x,self.y)
            self.remove = 0
        def collision(self):
            for f in bullets:
                if self.rect.colliderect(f.rect):
                    pygame.mixer.Sound.play(wallsound)
                    self.remove=1
                    self.hp-=1
                    bullets.remove(f)
            if self.hp==0:
                for w in walls:
                    if self.rect.colliderect(w.rect):
                        walls.remove(w)
        def draw(self):
            if self.hp==2:
                old_center = self.rect.center
                new = pygame.transform.rotate(self.walls,90)
                self.rect = new.get_rect()
                self.rect.center = old_center
                window.blit(new, self.rect)
            elif self.hp==1:
                old_center = self.rect.center
                new = pygame.transform.rotate(self.walls2,90)
                self.rect = new.get_rect()
                self.rect.center = old_center
                window.blit(new, self.rect)
    class Food():
        def __init__(self,x,y):
            self.x=x
            self.y=y
            self.remove=0
            self.foods=foodimage 
            self.size=24
            self.hp=1
            self.rect = self.foods.get_rect()
            self.rect.center = (self.x,self.y)
        def collision(self):
            for f in bullets:
                if self.rect.colliderect(f.rect):
                    self.remove=1
                    self.hp-=1
                    bullets.remove(f)
            if self.hp==0:
                for f in foods:
                    if self.rect.colliderect(f.rect):
                        foods.remove(f)
        def draw(self):
            old_center = self.rect.center
            new = pygame.transform.rotate(self.foods,90)
            self.rect = new.get_rect()
            self.rect.center = old_center
            window.blit(new, self.rect)
    
    bullets = []
    walls=[]
    foods=[]
    tank = Tank()
    tank2=Tank2()
    fps = pygame.time.Clock()
    mil=fps.tick(30)
    sec=mil/1000
    run = 1
    emag=True
    timer=0
    timer2=0
    gmg=False
    while run:

        timer+=1
        
        for f in pygame.event.get():
            if f.type == pygame.QUIT:
                run = 0
            if f.type==pygame.KEYDOWN:
                
                if f.key == pygame.K_ESCAPE:
                    pygame.mixer.Sound.play(menuselect)
                    run=0
                    gamemenu.menu()
               
        k = pygame.key.get_pressed()
        window.fill((155,155,155))
        if gmg==False:
            tank.move(k,sec)
            tank2.move(k,sec)
            tank.rotate(k)
            tank2.rotate(k)
            tank.draw()
            tank2.draw()           
        i=random.randint(1,40)
        j=random.randint(1,60)  
        l=random.randint(1,25)
        M=random.randint(1,45)  
        k=random.randint(1,100)
        if k==1:
            walls.append(Wall(j*16,i*16))
        if timer%150==0:

            foods.append(Food(M*24,l*24)) 
        if  tank.food_dir==True:
            timer2+=1
            if timer2==150:
                tank.vel=100
                tank2.vel=100
                tank.food_dir=False
                timer2=0
                print('ex')

            
        window.blit(Font.render(f"Hp:{tank.hp}",1,(0,255,0)),(0,0))
        window.blit(Font.render(f"Hp:{tank2.hp}",1,(255,0,0)),(960,0))
        if tank.hp<=0:
            gmg=True
            window.blit(gameover,(300,0))
        if tank2.hp<=0:
            gmg=True
            window.blit(gameover,(300,0))
        if gmg==False:
            for f in walls:
                f.draw()
                f.collision()
            for f in foods:
                f.draw()
                f.collision()
        
            for f in bullets:
                f.move()
                f.draw()
           
        
        
        pygame.display.update()
        fps.tick(30)
        if gmg==True:
            for f in pygame.event.get():
                if f.type == pygame.QUIT:
                    run = 0
                if f.type==pygame.KEYDOWN:
                    
                    if f.key == pygame.K_ESCAPE:
                        pygame.mixer.Sound.play(menuselect)
                        run=0
                        gamemenu.menu()
            if emag==True:
                pygame.mixer.Sound.play(gameover_sound)
                emag=False
            
            for f in pygame.event.get():
                if f.type==pygame.KEYDOWN:
                   if f.key == pygame.K_r:
                        pygame.mixer.Sound.play(menuselect)
                        tank.hp=3
                        tank.x=200
                        tank.y=200
                        tank.angle=0
                        tank.anglegun=180
                        tank2.hp=3
                        tank2.x=400
                        tank2.y=400
                        tank2.angle=0
                        tank2.anglegun=180
                        gmg=False
                        bullets=[]
                        walls=[]
                        foods=[]
                        pygame.mixer.Sound.stop(gameover_sound)
                        emag=True


        
    
    pygame.quit()
def Multi_tank():
    
    IP='34.254.177.17'
    PORT='5672'
    VHOST='dar-tanks'
    USER='dar-tanks'
    PASSWORD='5orPLExUYnyVYZg48caMpX'
    pygame.init()
    window=pygame.display.set_mode((1000, 600))
    class TankRpcClient(Thread):
        def __init__(self):
            self.connection=pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=IP,
                    port=PORT,
                    virtual_host=VHOST,
                    credentials=pika.PlainCredentials(
                        username=USER,
                        password=PASSWORD
                    )
                )
            )
            self.channel=self.connection.channel()
            queue=self.channel.queue_declare(queue='',auto_delete=True,exclusive=True)
            self.callback_queue=queue.method.queue
            self.channel.queue_bind(exchange='X:routing.topic',queue=self.callback_queue)
            self.channel.basic_consume(
                queue=self.callback_queue,
                on_message_callback=self.on_response,
                auto_ack=True)
            self.response=None
            self.corr_id=None
            self.token=None
            self.tank_id=None
            self.room_id=None
            self.bullet_id=None
            
        def on_response(self, ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = json.loads(body) 
                print(self.response)   
        def call(self, key,message={}):
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(
                exchange='X:routing.topic',
                routing_key=key,
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id,
                ),
                body=json.dumps(message))
            while self.response is None:
                self.connection.process_data_events()
            
        def check_server_status(self):
            self.call('tank.request.healthcheck')
        def obtain_token(self,room_id):
            message={
                'roomId':room_id
            }
            self.call('tank.request.register',message)
            if 'token' in self.response:
                self.token=self.response['token']
                self.tank_id=self.response['tankId']
                self.room_id=self.response['roomId']
        def turn_tank(self,token,direction):
            message={
                'token':token,
                'direction':direction
            }
            self.call('tank.request.turn',message)
        def fire_bullet(self,token):
            message={
                'token':token
            }
            self.call('tank.request.fire',message)
            if 'token' in self.response:
                self.bullet_id=self.response['owner']

    class TankConsumerClient(Thread):
        def __init__(self,room_id):
            super().__init__()
            self.connection=pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=IP,
                    port=PORT,
                    virtual_host=VHOST,
                    credentials=pika.PlainCredentials(
                        username=USER,
                        password=PASSWORD
                    )
                )
            )
            self.channel=self.connection.channel()
            queue=self.channel.queue_declare(queue='',auto_delete=True,exclusive=True)
            event_listener=queue.method.queue
            self.channel.queue_bind(exchange='X:routing.topic',
                                    queue=event_listener,
                                    routing_key='event.state.room-10')
            self.channel.basic_consume(queue=event_listener,on_message_callback=self.on_response,auto_ack=True)
            self.response=None    
        def on_response(self, ch, method, props, body):
            self.response = json.loads(body)
            
            
            
        def run(self):
            self.channel.start_consuming() 
        def close(self):
            self.channel.close() 
    client=TankRpcClient()
    client.check_server_status()
    client.obtain_token('room-10')
    
    
    event_client=TankConsumerClient('room-10')
    event_client.start()
    def draw_tank(x,y,width,height,direction,tank_id,health_id):
        body=MEtank
        body2=Mtank
        
        nick = Font.render(tank_id,1,(0,0,0))
        nick2=Font.render(client.tank_id,1,(0,0,0))
        nick3=Font.render(str(health_id),1,(0,0,0))
        rect=body.get_rect()
        rect2=body.get_rect()
        rect.center = (x+int(width/2),y+int(height/2))
        rect2.center=(x+int(width/2),y+int(height/2))
        angle=180
        if client.tank_id!=tank_id:
            if direction=='DOWN':
                pygame.mixer.Sound.play(moves)
                angle=90      
                          
            elif direction=='UP':
                pygame.mixer.Sound.play(moves)
                angle=270
                  
            elif direction=='LEFT':
                pygame.mixer.Sound.play(moves)
                angle=0
                
            elif direction=='RIGHT':
                pygame.mixer.Sound.play(moves)
                angle=180

                
                
            old_center = rect.center
            new = pygame.transform.rotate(body,angle)
            rect = new.get_rect()
            rect.center = old_center
            window.blit(new,rect)    
            if direction=='DOWN':
                window.blit(nick,(x-15,y-20))
                       
            else:
                window.blit(nick,(x-15,y+25))       
            if direction=='LEFT':

                window.blit(nick3,(x+35,y+10))
            else :
   
                window.blit(nick3,(x-15,y+10))
        else:
            if direction=='DOWN':
                pygame.mixer.Sound.play(moves)
                angle2=90
            elif direction=='UP':
                pygame.mixer.Sound.play(moves)
                angle2=270      
            elif direction=='LEFT':
                pygame.mixer.Sound.play(moves)
                angle2=0
            elif direction=='RIGHT':
                pygame.mixer.Sound.play(moves)
                angle2=180
            old_center = rect2.center
            new = pygame.transform.rotate(body2,angle2)
            rect2 = new.get_rect()
            rect2.center = old_center
            window.blit(new,rect2)
            if direction=='DOWN':
                window.blit(nick2,(x-15,y-20))         
            else:
                window.blit(nick2,(x-15,y+25))  


    def draw_bullet(x,y,width,height,direction,bullet_id):
        
        
        body=Mbullet
        body2=Mbullet
        rect=body.get_rect()
        rect2=body2.get_rect()
        rect.center = (x+int(width/2),y+int(height/2))
        rect2.center = (x+int(width/2),y+int(height/2))
        angle=180
        if client.bullet_id!=bullet_id:
            if direction=='DOWN':
                angle=90               
            elif direction=='UP':
                angle=270
            elif direction=='LEFT':
                angle=0
            elif direction=='RIGHT':
                angle=180
            old_center = rect.center
            new = pygame.transform.rotate(body,angle)
            rect = new.get_rect()
            rect.center = old_center
            window.blit(new,rect) 
        else:
            if direction=='DOWN':
                angle2=90
            elif direction=='UP':
                angle2=270      
            elif direction=='LEFT':
                angle2=0
            elif direction=='RIGHT':
                angle2=180
            old_center = rect2.center
            new = pygame.transform.rotate(body2,angle2)
            rect2 = new.get_rect()
            rect2.center = old_center
            window.blit(new,rect2)
    def info_table(healthcheck,score,tank_id):
        if client.tank_id==tank_id:
            myhealth=Font.render('My health:{}'.format(healthcheck),True,(255,255,255))
            myhealth_rect=myhealth.get_rect()
            myhealth_rect.center=(915,45)
            window.blit(myhealth,myhealth_rect)
            myscore=Font.render('My score:{}'.format(score),True,(255,255,255))
            myscore_rect=myscore.get_rect()
            myscore_rect.center=(915,65)
            window.blit(myscore,myscore_rect)



    

   
    UP='UP'
    DOWN='DOWN'
    LEFT='LEFT'
    RIGHT='RIGHT'
    MOVE_KEYS={
        pygame.K_w: UP,
        pygame.K_s: DOWN,
        pygame.K_a: LEFT,
        pygame.K_d: RIGHT
    }
    SPACE='SPACE'
    FIRE_KEYS={
        pygame.K_SPACE: SPACE
    }
    run=True
    gmg=False
    data={}
    data_win={}
    data_lose={}
    data_kicked={}
    while run:

        window.fill((0,250,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                event_client.close()
                run=False
                
                
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print(data_lose)
                    event_client.close()
                    run = False
                    gamemenu.menu()  
                    pygame.mixer.Sound.play(menuselect)

                    
                    
                    
                                      
                if event.key in MOVE_KEYS:
                    client.turn_tank(client.token,MOVE_KEYS[event.key])
                if event.key in FIRE_KEYS:
                    pygame.mixer.Sound.stop(moves)
                    pygame.mixer.Sound.play(soundbullet)
                    client.fire_bullet(client.token)

                 
        
        
        try:
            hits=event_client.response['hits']
            bullets=event_client.response['gameField']['bullets']
            winners=event_client.response['winners']
            losers=event_client.response['losers']
            kicked=event_client.response['kicked']
            remaining_time=event_client.response['remainingTime']
            tanks=event_client.response['gameField']['tanks']
            timer=Font.render('Remaining time:{}'.format(remaining_time),True,(255,255,255))
            timer_rect=timer.get_rect()
            timer_rect.center=(915,30)
            timer2=Font.render('Losers:',True,(255,255,255))
            timer2_rect=timer2.get_rect()
            timer2_rect.center=(915,230)
            timer3=Font.render('Kicked:',True,(255,255,255))
            timer3_rect=timer3.get_rect()
            timer3_rect.center=(915,400)
            window.blit(timer,timer_rect)
            window.blit(timer2,timer2_rect)
            window.blit(timer3,timer3_rect)
            if remaining_time==0:
                pygame.mixer.Sound.stop(moves)
                window.blit(timeover,(0,0))
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_r:
                        pygame.mixer.Sound.play(menuselect)


                        Multi_tank()   
            for win in winners:
                win_tank=win['tankId']
                win_score=win['score']
                data_win[win_tank]=win_score
                data_win={k :v for k,v in sorted(data_win.items(),key=lambda item:item[1],reverse=True)}

                
             
            for lose in losers:
                lose_tank=lose['tankId']
                lose_score=lose['score']
                data_lose[lose_tank]=lose_score
                data_lose={k :v for k,v in sorted(data_lose.items(),key=lambda item:item[1],reverse=True)}
  
            for kick in kicked:
                kick_tank=kick['tankId']
                kick_score=kick['score']
                data_kicked[kick_tank]=kick_score
                data_kicked={k :v for k,v in sorted(data_kicked.items(),key=lambda item:item[1],reverse=True)} 
                 
            for tank in tanks:
            
                
                tank_health=tank['health']
                tank_score=tank['score']
                tank_id=tank['id']
                tank_x=tank['x']
                tank_y=tank['y']
                tank_width=tank['width']
                tank_height=tank['height']
                tank_direction=tank['direction']
            
                data[tank_id]=tank_score
                data={k :v for k,v in sorted(data.items(),key=lambda item:item[1],reverse=True)}
                if tank['id']==client.tank_id:
                    data.pop(tank_id)
                
                draw_tank(tank_x,tank_y,tank_width,tank_height,tank_direction,tank_id,tank_health)
                info_table(tank_health,tank_score,tank_id)
                k=915
                l=85
                for f,g in data.items():
                    ID = Font.render('{}'.format(f),True,(255,255,255))
                    Score=Font.render('{}'.format(g),True,(255,255,255))                
                    ID_rect=ID.get_rect()
                    ID_rect.center=(k,l)
                    window.blit(ID,ID_rect)
                    Score_rect=Score.get_rect()
                    Score_rect.center=(k+50,l)
                    window.blit(Score,Score_rect)
                    l+=20  
            
            for hit in hits:
                hit_sourse=hit['sourse']
                hit_destination=hit['destination']            
               
            for bullet in bullets:

                bullet_id=bullet['owner']
                bullet_x=bullet['x']
                bullet_y=bullet['y']
                bullet_w=bullet['width']
                bullet_h=bullet['height']
                bullet_dir=bullet['direction']
                draw_bullet(bullet_x,bullet_y,bullet_w,bullet_h,bullet_dir,bullet_id)
                if bullet_id==hit_sourse:
                    pygame.mixer.Sound.stop(moves)
                    pygame.mixer.Sound.play(soundbullet)                                         
            k=915
            m=230
            l=400                            

                
            for f,g in data_kicked.items():
                l+=20
                ID = Font.render('{}'.format(f),True,(255,255,255))
                Score=Font.render('{}'.format(g),True,(255,255,255))                
                ID_rect=ID.get_rect()
                ID_rect.center=(k,l)
                window.blit(ID,ID_rect)
                Score_rect=Score.get_rect()
                Score_rect.center=(k+50,l)
                window.blit(Score,Score_rect)
            for f,g in data_lose.items():
                m+=20 
                ID = Font.render('{}'.format(f),True,(255,255,255))
                Score=Font.render('{}'.format(g),True,(255,255,255))                
                ID_rect=ID.get_rect()
                ID_rect.center=(k,m)
                window.blit(ID,ID_rect)
                Score_rect=Score.get_rect()
                Score_rect.center=(k+50,m)
                window.blit(Score,Score_rect)  
            for f,g in data_lose.items():
                if f==client.tank_id:
                    pygame.mixer.Sound.stop(moves)
                    mscore=Font.render('Your Score:{}'.format(g),True,(255,255,255))
                    mscore_rect=mscore.get_rect()
                    mscore_rect.center=(300,350)
                    window.blit(youlose,(0,0))
                    window.blit(mscore,mscore_rect)
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key==pygame.K_r:
                            pygame.mixer.Sound.play(menuselect)

                            Multi_tank()
            for f,g in data_won.items():
                if f==client.tank_id:
                    pygame.mixer.Sound.stop(moves)
                    mscore=Font.render('Your Score:{}'.format(g),True,(255,255,255))
                    mscore_rect=mscore.get_rect()
                    mscore_rect.center=(300,350)
                    window.blit(youwon,(0,0))
                    window.blit(mscore,mscore_rect)
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key==pygame.K_r:
                            pygame.mixer.Sound.play(menuselect)


                            Multi_tank()
          
           
        

               
        except:
            pass
        line=pygame.draw.rect(window,(0,0,0),(825,0,10,600))
        
        pygame.display.flip()
    client.connection.close()
    pygame.quit()

def Multi_AI():
    IP='34.254.177.17'
    PORT='5672'
    VHOST='dar-tanks'
    USER='dar-tanks'
    PASSWORD='5orPLExUYnyVYZg48caMpX'
    pygame.init()
    window=pygame.display.set_mode((1000, 600))
    class TankRpcClient(Thread):
        def __init__(self):
            self.connection=pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=IP,
                    port=PORT,
                    virtual_host=VHOST,
                    credentials=pika.PlainCredentials(
                        username=USER,
                        password=PASSWORD
                    )
                )
            )
            self.channel=self.connection.channel()
            queue=self.channel.queue_declare(queue='',auto_delete=True,exclusive=True)
            self.callback_queue=queue.method.queue
            self.channel.queue_bind(exchange='X:routing.topic',queue=self.callback_queue)
            self.channel.basic_consume(
                queue=self.callback_queue,
                on_message_callback=self.on_response,
                auto_ack=True)
            self.response=None
            self.corr_id=None
            self.token=None
            self.tank_id=None
            self.room_id=None
            self.bullet_id=None
            
        def on_response(self, ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = json.loads(body) 
                print(self.response)   
        def call(self, key,message={}):
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(
                exchange='X:routing.topic',
                routing_key=key,
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id,
                ),
                body=json.dumps(message))
            while self.response is None:
                self.connection.process_data_events()
            
        def check_server_status(self):
            self.call('tank.request.healthcheck')
        def obtain_token(self,room_id):
            message={
                'roomId':room_id
            }
            self.call('tank.request.register',message)
            if 'token' in self.response:
                self.token=self.response['token']
                self.tank_id=self.response['tankId']
                self.room_id=self.response['roomId']
        def turn_tank(self,token,direction):
            message={
                'token':token,
                'direction':direction
            }
            self.call('tank.request.turn',message)
        def fire_bullet(self,token):
            message={
                'token':token
            }
            self.call('tank.request.fire',message)
            if 'token' in self.response:
                self.bullet_id=self.response['owner']

    class TankConsumerClient(Thread):
        def __init__(self,room_id):
            super().__init__()
            self.connection=pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=IP,
                    port=PORT,
                    virtual_host=VHOST,
                    credentials=pika.PlainCredentials(
                        username=USER,
                        password=PASSWORD
                    )
                )
            )
            self.channel=self.connection.channel()
            queue=self.channel.queue_declare(queue='',auto_delete=True,exclusive=True)
            event_listener=queue.method.queue
            self.channel.queue_bind(exchange='X:routing.topic',queue=event_listener,routing_key='event.state.room-10')
            self.channel.basic_consume(queue=event_listener,on_message_callback=self.on_response,auto_ack=True)
            self.response=None    
        def on_response(self, ch, method, props, body):
            self.response = json.loads(body)
            
            
            
        def run(self):
            self.channel.start_consuming() 
        def close(self):
            self.channel.close() 
    
    client=TankRpcClient()
    client.check_server_status()
    client.obtain_token('room-10')
    client.turn_tank(client.token,'DOWN')
    
    event_client=TankConsumerClient('room-10')
    event_client.start()
    def draw_tank(x,y,width,height,direction,tank_id,health_id):
        body=MEtank
        body2=Mtank
        
        nick = Font.render(tank_id,1,(0,0,0))
        nick2=Font.render(client.tank_id,1,(0,0,0))
        nick3=Font.render(str(health_id),1,(0,0,0))
        rect=body.get_rect()
        rect2=body.get_rect()
        rect.center = (x+int(width/2),y+int(height/2))
        rect2.center=(x+int(width/2),y+int(height/2))
        angle=180
        if client.tank_id!=tank_id:
            if direction=='DOWN':
                pygame.mixer.Sound.play(moves)
                angle=90      
                          
            elif direction=='UP':
                pygame.mixer.Sound.play(moves)
                angle=270
                  
            elif direction=='LEFT':
                pygame.mixer.Sound.play(moves)
                angle=0
                
            elif direction=='RIGHT':
                pygame.mixer.Sound.play(moves)
                angle=180

                
                
            old_center = rect.center
            new = pygame.transform.rotate(body,angle)
            rect = new.get_rect()
            rect.center = old_center
            window.blit(new,rect)    
            if direction=='DOWN':
                window.blit(nick,(x-15,y-20))
                       
            else:
                window.blit(nick,(x-15,y+25))       
            if direction=='LEFT':

                window.blit(nick3,(x+35,y+10))
            else :
   
                window.blit(nick3,(x-15,y+10))
        else:
            if direction=='DOWN':
                pygame.mixer.Sound.play(moves)
                angle2=90
            elif direction=='UP':
                pygame.mixer.Sound.play(moves)
                angle2=270      
            elif direction=='LEFT':
                pygame.mixer.Sound.play(moves)
                angle2=0
            elif direction=='RIGHT':
                pygame.mixer.Sound.play(moves)
                angle2=180
            old_center = rect2.center
            new = pygame.transform.rotate(body2,angle2)
            rect2 = new.get_rect()
            rect2.center = old_center
            window.blit(new,rect2)
            if direction=='DOWN':
                window.blit(nick2,(x-15,y-20))         
            else:
                window.blit(nick2,(x-15,y+25))  


    def draw_bullet(x,y,width,height,direction,bullet_id):
        
        
        body=Mbullet
        body2=Mbullet
        rect=body.get_rect()
        rect2=body2.get_rect()
        rect.center = (x+int(width/2),y+int(height/2))
        rect2.center = (x+int(width/2),y+int(height/2))
        angle=180
        if client.bullet_id!=bullet_id:
            if direction=='DOWN':
                angle=90               
            elif direction=='UP':
                angle=270
            elif direction=='LEFT':
                angle=0
            elif direction=='RIGHT':
                angle=180
            old_center = rect.center
            new = pygame.transform.rotate(body,angle)
            rect = new.get_rect()
            rect.center = old_center
            window.blit(new,rect) 
        else:
            if direction=='DOWN':
                angle2=90
            elif direction=='UP':
                angle2=270      
            elif direction=='LEFT':
                angle2=0
            elif direction=='RIGHT':
                angle2=180
            old_center = rect2.center
            new = pygame.transform.rotate(body2,angle2)
            rect2 = new.get_rect()
            rect2.center = old_center
            window.blit(new,rect2)
    def info_table(healthcheck,score,tank_id):
        if client.tank_id==tank_id:
            myhealth=Font.render('My health:{}'.format(healthcheck),True,(255,255,255))
            myhealth_rect=myhealth.get_rect()
            myhealth_rect.center=(915,45)
            window.blit(myhealth,myhealth_rect)
            myscore=Font.render('My score:{}'.format(score),True,(255,255,255))
            myscore_rect=myscore.get_rect()
            myscore_rect.center=(915,65)
            window.blit(myscore,myscore_rect)


    
    direct='' 
    ctimer=0
    UP='UP'
    DOWN='DOWN'
    LEFT='LEFT'
    RIGHT='RIGHT'

    run=True
    gmg=False
    shot=False
    data={}
    data_win={}
    data_lose={}
    data_kicked={}
    while run:
        ctimer+=1
        window.fill((0,250,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                event_client.close()
                run=False
                
                
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print(data_lose)
                    event_client.close()
                    run = False
                    gamemenu.menu()  
                    pygame.mixer.Sound.play(menuselect)

                    
                    
                    
                                      
                # if event.key in MOVE_KEYS:
                #     client.turn_tank(client.token,MOVE_KEYS[event.key])
                # if event.key in FIRE_KEYS:
                #     pygame.mixer.Sound.stop(moves)
                #     pygame.mixer.Sound.play(soundbullet)
                #     client.fire_bullet(client.token)

                 
        
        
        try:
            hits=event_client.response['hits']
            bullets=event_client.response['gameField']['bullets']
            winners=event_client.response['winners']
            losers=event_client.response['losers']
            kicked=event_client.response['kicked']
            remaining_time=event_client.response['remainingTime']
            tanks=event_client.response['gameField']['tanks']
            timer=Font.render('Remaining time:{}'.format(remaining_time),True,(255,255,255))
            timer_rect=timer.get_rect()
            timer_rect.center=(915,30)
            timer2=Font.render('Losers:',True,(255,255,255))
            timer2_rect=timer2.get_rect()
            timer2_rect.center=(915,230)
            timer3=Font.render('Kicked:',True,(255,255,255))
            timer3_rect=timer3.get_rect()
            timer3_rect.center=(915,400)
            window.blit(timer,timer_rect)
            window.blit(timer2,timer2_rect)
            window.blit(timer3,timer3_rect)
            if remaining_time==0:
                pygame.mixer.Sound.stop(moves)
                window.blit(timeover,(0,0))
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_r:
                        pygame.mixer.Sound.play(menuselect)


                        Multi_tank()   
            for win in winners:
                win_tank=win['tankId']
                win_score=win['score']
                data_win[win_tank]=win_score
                data_win={k :v for k,v in sorted(data_win.items(),key=lambda item:item[1],reverse=True)}

                
             
            for lose in losers:
                lose_tank=lose['tankId']
                lose_score=lose['score']
                data_lose[lose_tank]=lose_score
                data_lose={k :v for k,v in sorted(data_lose.items(),key=lambda item:item[1],reverse=True)}
  
            for kick in kicked:
                kick_tank=kick['tankId']
                kick_score=kick['score']
                data_kicked[kick_tank]=kick_score
                data_kicked={k :v for k,v in sorted(data_kicked.items(),key=lambda item:item[1],reverse=True)} 
                 
            for tank in tanks:
            
                
                tank_health=tank['health']
                tank_score=tank['score']
                tank_id=tank['id']
                tank_x=tank['x']
                tank_y=tank['y']
                tank_width=tank['width']
                tank_height=tank['height']
                tank_direction=tank['direction']
                if tank['id']==client.tank_id:
                    my_x=tank_x
                    my_y=tank_y
                x1=my_x
                y1=my_y
                x=tank_x
                y=tank_y
                
                
                if tank_id!=client.tank_id:
                    for i in range(x1,x1+32):                       
                            if x==i:
                                if y>y1:
                                    direct='UP'
                                    shot=True
                                elif y<=y1:
                                    
                                    direct='Down'
                                    shot=True
                    for i in range(y1,y1+32):
                            if x==i:
                                if x1>x:
                                    direct='RIGHT'
                                    
                                    shot=True
                                elif x1<=x:
                                    direct='LEFT'
                                    
                                    shot=True 
                client.turn_tank(client.token,direct) 
                if shot==True:
                    
                        pygame.mixer.Sound.stop(moves)
                        pygame.mixer.Sound.play(soundbullet)
                        client.fire_bullet(client.token) 
                        shot=False
                                
                    

                data[tank_id]=tank_score
                data={k :v for k,v in sorted(data.items(),key=lambda item:item[1],reverse=True)}
                if tank['id']==client.tank_id:
                    data.pop(tank_id)
                
                draw_tank(tank_x,tank_y,tank_width,tank_height,tank_direction,tank_id,tank_health)
                info_table(tank_health,tank_score,tank_id)
                k=915
                l=85
                for f,g in data.items():
                    ID = Font.render('{}'.format(f),True,(255,255,255))
                    Score=Font.render('{}'.format(g),True,(255,255,255))                
                    ID_rect=ID.get_rect()
                    ID_rect.center=(k,l)
                    window.blit(ID,ID_rect)
                    Score_rect=Score.get_rect()
                    Score_rect.center=(k+50,l)
                    window.blit(Score,Score_rect)
                    l+=20  
            
            for hit in hits:
                hit_sourse=hit['sourse']
                hit_destination=hit['destination']            
               
            for bullet in bullets:

                bullet_id=bullet['owner']
                bullet_x=bullet['x']
                bullet_y=bullet['y']
                bullet_w=bullet['width']
                bullet_h=bullet['height']
                bullet_dir=bullet['direction']
                draw_bullet(bullet_x,bullet_y,bullet_w,bullet_h,bullet_dir,bullet_id)
                if bullet_id==hit_sourse:
                    pygame.mixer.Sound.stop(moves)
                    pygame.mixer.Sound.play(soundbullet)                                         
            k=915
            m=230
            l=400  
 
                
            for f,g in data_kicked.items():
                l+=20
                ID = Font.render('{}'.format(f),True,(255,255,255))
                Score=Font.render('{}'.format(g),True,(255,255,255))                
                ID_rect=ID.get_rect()
                ID_rect.center=(k,l)
                window.blit(ID,ID_rect)
                Score_rect=Score.get_rect()
                Score_rect.center=(k+50,l)
                window.blit(Score,Score_rect)
            for f,g in data_lose.items():
                m+=20 
                ID = Font.render('{}'.format(f),True,(255,255,255))
                Score=Font.render('{}'.format(g),True,(255,255,255))                
                ID_rect=ID.get_rect()
                ID_rect.center=(k,m)
                window.blit(ID,ID_rect)
                Score_rect=Score.get_rect()
                Score_rect.center=(k+50,m)
                window.blit(Score,Score_rect)  
            for f,g in data_lose.items():
                if f==client.tank_id:
                    pygame.mixer.Sound.stop(moves)
                    mscore=Font.render('Your Score:{}'.format(g),True,(255,255,255))
                    mscore_rect=mscore.get_rect()
                    mscore_rect.center=(300,350)
                    window.blit(youlose,(0,0))
                    window.blit(mscore,mscore_rect)
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key==pygame.K_r:
                            pygame.mixer.Sound.play(menuselect)

                            Multi_tank()
            for f,g in data_won.items():
                if f==client.tank_id:
                    pygame.mixer.Sound.stop(moves)
                    mscore=Font.render('Your Score:{}'.format(g),True,(255,255,255))
                    mscore_rect=mscore.get_rect()
                    mscore_rect.center=(300,350)
                    window.blit(youwon,(0,0))
                    window.blit(mscore,mscore_rect)
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key==pygame.K_r:
                            pygame.mixer.Sound.play(menuselect)


                            Multi_tank()
          
           
        

               
        except:
            pass
        line=pygame.draw.rect(window,(0,0,0),(825,0,10,600))
        
        pygame.display.flip()
    client.connection.close()
    pygame.quit()  


items=[(200,140,u'Single Player',(250,250,30),(250,30,250),0),
        (200,200,u'Multi Player',(250,250,30),(250,30,250),1),
        (200,260,u'Multi AI Player',(250,250,30),(250,30,250),2),
        (200,320,u'Quit',(250,250,30),(250,30,250),3)]
gamemenu=Menu(items)
gamemenu.menu()

