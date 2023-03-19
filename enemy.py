import pygame
import os
import random
import time
from pygame.locals import *

pygame.font.init()

vec = pygame.math.Vector2


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

LASER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('healthbar','laser.png')),(300,400))
class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = LASER_IMG
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.x += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

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

class Player:
    def __init__(self,x,y,health = 1000):
        self.player_img = PLAYER
        self.x = x
        self.y = y
        self.health = health
        self.mask = pygame.mask.from_surface(self.player_img)
    def draw(self,window):
        window.blit(self.player_img,(self.x,self.y))
    def collision(self,obj):
        return collide(self,obj)

def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y 
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None    
def main():
    enemies = [] 
    laser = []
    lost = False
    lives = 3
    player = Player(750,700)
    take_damage = 1
    health = 2
    scores = 0 
    laser_num = 1

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
        WIN.blit(scores_label, (1140, 3))
        player.draw(WIN)

        for laser_player in laser :
            laser_player.draw(WIN)

        for enemFromRight in enemies :
            enemFromRight.draw(WIN)

        health_bar = HealthBar(10,10,health)
        health_bar.render(WIN)
        pygame.display.update()

    wave_length = 5

    enemy_vel = 5
    enemy_vel = float(enemy_vel)
    clock = pygame.time.Clock()
    run = True 
    while run :
        laser_num += 1
        lost_count = 0
        lost_font = pygame.font.SysFont("comicsans",200)
        clock.tick(FPS)
        if  len(enemies) == 0 :
            enemy_vel += 0.5
            wave_length += 5
            for n in range(1):
                laser_player = Laser(700,400)
                laser.append(laser_player)
            for i in range(wave_length):
                enemFromRight = Enemy(random.randrange(1550,3000),random.randrange(500,800))   
                enemies.append(enemFromRight)

        for laser_player in laser[:]:
            laser_player.move(enemy_vel)

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False
        
        for enemFromRight in enemies[:]:
            enemFromRight.move(enemy_vel)
            if enemFromRight.x + enemFromRight.get_width() < 50:
                # lost == True
                enemies.remove(enemFromRight)

            if collide(enemFromRight,player):
                health -= 1
                enemies.remove(enemFromRight)
                lives = lives - 1

        for enemFromRight in enemies[:]:
            for laser_player in laser[:]:
                if collide(laser_player,enemFromRight):
                    enemies.remove(enemFromRight)
                    laser.remove(laser_player)
                    scores += 1

        if lives == 0:
            WIN.blit(LAST_HEART,(10,10))
            lost = True
            lost_count += 1
        if lost:
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