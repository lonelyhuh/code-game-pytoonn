import pygame
import os
import random
import time
from pygame.locals import *

pygame.font.init()

vec = pygame.math.Vector2

#set up

WIDTH = 1550
HEIGHT = 820
BLACK = (0,0,0)
WHITE = (255,255,255)
X,Y = 40,50
PLAYER = pygame.transform.scale(pygame.image.load(os.path.join('tai nguyen','monster.png')),(X+50,Y+40))
FPS = 160
ENEMY_IMG = pygame.transform.scale(pygame.image.load(os.path.join('tai nguyen','monster 2.png')),(X,Y))
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) 
pygame.display.set_caption('dong anh dzai 102')
LAST_HEART = pygame.image.load(os.path.join('healthbar','heart4.png'))

BG = pygame.transform.scale(pygame.image.load(os.path.join("healthbar", "backgroundreal.png")), (WIDTH, HEIGHT))
BG_START = pygame.transform.scale(pygame.image.load(os.path.join('healthbar','bg3.jpg')),(WIDTH,HEIGHT))
BG_RESTART = pygame.transform.scale(pygame.image.load(os.path.join('healthbar','bg4.jpg')),(WIDTH,HEIGHT))

CHARACTER_1 = pygame.image.load(os.path.join('healthbar','character1.png'))
CHARACTER_2 = pygame.image.load(os.path.join('healthbar','character2.png'))
CHARACTER_3 = pygame.image.load(os.path.join('healthbar','character3.png'))

velocity_y = 0
gravity = 0.5
# moving_sprite=pygame.sprite.Group()
# player=Player(100,100)
# moving_sprite.add(player)
class HealthBar :
    def __init__(self, x, y,health):
        super().__init__()

        self.load_animations()

        self.health = health 
        self.image = self.health_animations[self.health]
        self.pos = vec(x, y)

    def render(self, display):
        display.blit(self.image, self.pos)

    def takeDamage(self, damage = 1 ):
        self.health -= damage
        if self.health < 0: self.health = 0
        
        self.image = self.health_animations[self.health]
        
    def Heal(self, heal):
        self.health += damage
        if self.health > 30: self.health = 3
        
        self.image = self.health_animations[self.health]

    def load_animations(self):
        
        self.health_animations = [pygame.image.load("D:/codenek/healthbar/heart1.png").convert_alpha(),
                             pygame.image.load("D:/codenek/healthbar/heart2.png").convert_alpha(),
                             pygame.image.load("D:/codenek/healthbar/heart3.png").convert_alpha(),
                             pygame.image.load('D:/codenek/healthbar/heart4.png').convert_alpha()
                                    ]

class Enemy:
    def __init__(self,x,y,health = 100) :
        self.enemy_img = ENEMY_IMG
        self.x = x
        self.y = y
        self.health = health
        self.mask = pygame.mask.from_surface(self.enemy_img) 
    def move(self,vel):
        self.x -= vel
    def draw(self,window):
        window.blit(self.enemy_img,(self.x,self.y))
    def get_width(self):
        return self.enemy_img.get_width()
    def collision(self, obj):
        return collide(self, obj)

class Player(pygame.sprite.Sprite):
    def __init__(self,x, y) :
        super().__init__()
        self.back = False
        self.forward = False
        self.up = False
        self.is_animating=False
        self.sprites=[]
        self.sprites.append(CHARACTER_1)
        self.sprites.append(CHARACTER_2)
        self.sprites.append(CHARACTER_3)
        self.x = x
        self.y = y
        # self.sprites.append(pygame.image.load('attack_4.png'))
        # self.sprites.append(pygame.image.load('attack_5.png'))
        # self.sprites.append(pygame.image.load('attack_6.png'))
        # self.sprites.append(pygame.image.load('attack_7.png'))
        # self.sprites.append(pygame.image.load('attack_8.png'))
        # self.sprites.append(pygame.image.load('attack_9.png'))
        # self.sprites.append(pygame.image.load('attack_10.png'))
        self.current_sprite=0
        self.image=self.sprites[self.current_sprite]
        self.rect=self.image.get_rect(topleft=(x,y))
        self.mask = pygame.mask.from_surface(self.image)
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
            self.x = self.x-4
            self.rect=self.image.get_rect(topleft=(self.x,self.y))

        if self.forward == True:
            self.x = self.x+4
            self.rect=self.image.get_rect(topleft=(self.x,self.y))
        if self.up == True:
            velocity_y = -6
        self.y += velocity_y
        velocity_y += gravity
        self.rect=self.image.get_rect(topleft=(self.x,self.y))
        while self.y > 700:
            self.y = 700
            self.rect = self.image.get_rect(topleft=(self.x,self.y))
        if self.y < 300:
            velocity_y = 0
            self.y =300
            self.rect=self.image.get_rect(topleft=(self.x,self.y))
    
def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y 
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None  

def main():
    enemies = [] 
    laser = []
    lost = False
    lives = 3
    take_damage = 1
    health = 2
    scores = 0 
    laser_num = 1
    moving_sprite=pygame.sprite.Group()
    player=Player(100,700)
    moving_sprite.add(player)
    wave_length = 10
    enemy_vel = 5
    enemy_vel = float(enemy_vel)
    clock = pygame.time.Clock()

    def reset_game():
        run = True
        while run:
            subtext_font = pygame.font.SysFont("comicsans", 50)
            subtext_label =  subtext_font.render("press the mouse to restart", 1, (255,255,255))
            WIN.blit(BG_RESTART,(0,0))
            WIN.blit(subtext_label,(450,450))
            lost_label = lost_font.render("MÀY NGU", 1, (255,255,255))
            # subtext = lost_font.render('an vo',1,())
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 200))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main()
        pygame.quit()

    def draw_window() :
        scores_font = pygame.font.SysFont("comicsans", 70)
        scores_label =  scores_font.render(f"score : {scores}", 1, (255,255,255))
        WIN.blit(BG, (0,0))
        moving_sprite.draw(WIN)
        moving_sprite.update(0.3)
        WIN.blit(scores_label, (1140, 3))
        # player.draw(WIN)

        # for laser_player in laser :
        #     laser_player.draw(WIN)

        for enemFromRight in enemies :
            enemFromRight.draw(WIN)

        health_bar = HealthBar(10,10,health)
        health_bar.render(WIN)
        pygame.display.update()

    run = True 
    while run :
        laser_num += 1
        lost_count = 0
        lost_font = pygame.font.SysFont("comicsans",200)
        clock.tick(FPS)
        if  len(enemies) == 0 :
            enemy_vel += 0.5
            wave_length += 5
            # for n in range(1):
            #     laser_player = Laser(700,400)
            #     laser.append(laser_player)
            for i in range(wave_length):
                enemFromRight = Enemy(random.randrange(1550,3000),random.randrange(500,800))   
                enemies.append(enemFromRight)

        # for laser_player in laser[:]:
        #     laser_player.move(enemy_vel)

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False

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
        
        for enemFromRight in enemies[:]:
            enemFromRight.move(enemy_vel)
            if enemFromRight.x + enemFromRight.get_width() < 50:
                enemies.remove(enemFromRight)
                lost = True
            if collide(enemFromRight,player):
                health -= 1
                enemies.remove(enemFromRight)
                lives = lives - 1

        # for enemFromRight in enemies[:]:
        #     # for laser_player in laser[:]:
        #         if collide(laser_player,enemFromRight):
        #             enemies.remove(enemFromRight)
        #             # laser.remove(laser_player)
        #             scores += 1

            if lives == 0:
                WIN.blit(LAST_HEART,(10,10))
                lost = True
                lost_count += 1
            if lost == True:
                reset_game()
        draw_window()
    pygame.quit()
def main_menu():

    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG_START,(0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
main_menu()
