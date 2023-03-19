#bản mới nhất
import pygame,sys
import os
#tao lop nhan vat
class Player(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y) :
        super().__init__()
        self.back = False
        self.forward = False
        self.up = False
        self.is_animating=False
        self.sprites=[]
        self.sprites.append(pygame.image.load('character1.png'))
        self.sprites.append(pygame.image.load('character2.png'))
        self.sprites.append(pygame.image.load('character3.png'))
        self.pos_x = pos_x
        self.pos_y = pos_y
        # self.sprites.append(pygame.image.load('attack_4.png'))
        # self.sprites.append(pygame.image.load('attack_5.png'))
        # self.sprites.append(pygame.image.load('attack_6.png'))
        # self.sprites.append(pygame.image.load('attack_7.png'))
        # self.sprites.append(pygame.image.load('attack_8.png'))
        # self.sprites.append(pygame.image.load('attack_9.png'))
        # self.sprites.append(pygame.image.load('attack_10.png'))
        self.current_sprite=0
        self.image=self.sprites[self.current_sprite]
        self.rect=self.image.get_rect(topleft=(pos_x,pos_y))
    def atack(self):
        self.is_animating=True
    def lui(self):
        self.back = True
    def tien(self):
        self.forward = True
    def len(self):
    	self.up = True
    def update(self,speed):
        global velocity_y
        global gravity
        if self.is_animating==True:
            self.current_sprite+=speed
            if self.current_sprite>= len(self.sprites):
                self.current_sprite=0
                self.is_animating=False
        self.image=self.sprites[int(self.current_sprite)]
        if self.back == True:
            self.pos_x = self.pos_x-4
            self.rect=self.image.get_rect(topleft=(self.pos_x,self.pos_y))
        if self.forward == True:
            self.pos_x = self.pos_x+4
            self.rect=self.image.get_rect(topleft=(self.pos_x,self.pos_y))
        if self.up == True:
        	velocity_y = -4
        self.pos_y += velocity_y
        velocity_y += gravity
        self.rect=self.image.get_rect(topleft=(self.pos_x,self.pos_y))
        while self.pos_y > 100:
        	self.pos_y =100
        	self.rect=self.image.get_rect(topleft=(self.pos_x,self.pos_y))
        if self.pos_y < 5:
        	velocity_y = 0
        	self.pos_y =20
        	self.rect=self.image.get_rect(topleft=(self.pos_x,self.pos_y))


velocity_y = 0
gravity = 0.2
moving_sprite=pygame.sprite.Group()
player=Player(100,100)
moving_sprite.add(player)

pygame.init()

screen=pygame.display.set_mode((300,300))
pygame.display.set_caption('animation ech')
clock=pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_j:
                player.atack()
            elif event.key == pygame.K_a:
                player.lui()
            elif event.key == pygame.K_d:
            	player.tien()
            elif event.key == pygame.K_w:
            	player.len()

        if event.type==pygame.KEYUP:
            if event.key == pygame.K_a:
                player.back = False
            elif event.key == pygame.K_d:
            	player.forward = False
            elif event.key == pygame.K_w:
            	player.up = False


    screen.fill(('black'))
    moving_sprite.draw(screen)
    moving_sprite.update(0.3)
    pygame.display.flip()
    clock.tick(60)
