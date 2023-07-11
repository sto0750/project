# Shmup game
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl

# Music: Comet by Spiky Candy is licensed under a Creative Commons License.
# https://creativecommons.org/licenses/...
# Support by RFM - NCM: https://rb.gy/2h3zi

import pygame
import random
from os import path
import numpy as np

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')


WIDTH = 1800
HEIGHT = 1000
FPS = 60


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHOOT!")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, startingPosition):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        
        #self.image = pygame.Surface((30, 50))
        #self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = startingPosition[0]
        self.rect.bottom = startingPosition[1]
        self.speedx = 0
        self.speedy = 0
        self.accely = 0.5
        self.hp = 100
        self.cannon_type = 1
        self.cannon_angle = -90.
        self.cannon_anglespeed = 0.
        self.cannon_mag = 10.

    def rotate(self):
        self.cannon_angle = (self.cannon_angle + self.cannon_anglespeed) % 360
        new_image = pygame.transform.rotate(self.image_orig, -(self.cannon_angle+90))
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center


    def update(self):
        self.rotate()
        

        self.rect.x += self.speedx
        self.speedy += self.accely
        self.rect.y += self.speedy
        self.cannon_angle  += self.cannon_anglespeed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
    def shoot(self):
        vx = self.cannon_mag * np.cos(np.deg2rad(self.cannon_angle))
        vy = self.cannon_mag * np.sin(np.deg2rad(self.cannon_angle))
        if self.cannon_type == 1:
            cannonball = Cannonball1(self.rect.centerx, self.rect.centery, vx, vy)
            all_sprites.add(cannonball)
            cannonballs.add(cannonball)
                  

class Cannonball1(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self)

        #self.image = cannonball_img1
        #self.image.set_colorkey(BLACK)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = vy
        self.speedx = vx
        self.accely = 0.5

    def update(self):
        self.rect.x += self.speedx
        self.speedy += self.accely
        self.rect.y += self.speedy
        
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Terrrain(pygame.sprite.Sprite):
    def __init__(self,):
        pygame.sprite.Sprite.__init__(self)
        self.length = random.randrange(100, 200)
        self.image = pygame.Surface((self.length, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.length)
        self.rect.y = random.randrange(int(HEIGHT/3) , HEIGHT)
        
        #abcd



# Load all game graphics
cannon_img = pygame.image.load(path.join(img_dir, "cannon_img.png")).convert()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

# Game loop
game_over = True
running = True

all_sprites = pygame.sprite.Group()
cannonballs = pygame.sprite.Group()
terrains = pygame.sprite.Group()
players = pygame.sprite.Group()
for i in range(180):
    t = Terrrain()
    all_sprites.add(t)
    terrains.add(t)
player1 = Player((WIDTH/4. , 70))
player2 = Player((3*WIDTH/4., 70))
players.add(player1)
players.add(player2)

all_sprites.add(player1)
all_sprites.add(player2)

Turn = 1
# 1 for player1, 0 for player2

while running:
    if game_over:
        #show_go_screen()
        game_over = False
        
        #score = 0

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                if Turn == 1:
                    player1.shoot()
                elif Turn == 0 :
                    player2.shoot()
            elif event.key == pygame.K_UP:
                if Turn == 1:
                    player1.cannon_anglespeed -= 1.
                elif Turn == 0:
                    player2.cannon_anglespeed -= 1.
            elif event.key == pygame.K_DOWN:
                if Turn == 1:
                    player1.cannon_anglespeed += 1.
                elif Turn == 0:
                    player2.cannon_anglespeed += 1.
            elif event.key == pygame.K_LEFT:
                if Turn == 1:
                    player1.speedx = -2
                elif Turn == 0:
                    player2.speedx = -2
            elif event.key == pygame.K_RIGHT:
                if Turn == 1:
                    player1.speedx = 2
                elif Turn == 0:
                    player2.speedx = 2
            
            elif event.key == pygame.K_RETURN:
                Turn = (Turn + 1) % 2

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                if Turn == 1:
                    player1.cannon_anglespeed = 0
                elif Turn == 0:
                    player2.cannon_anglespeed = 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                if Turn == 1:
                    player1.speedx = 0
                elif Turn == 0:
                    player2.speedx = 0


    # Update
    
    all_sprites.update()

    # check to see if the player lands on a terrain.
    for p in players :
        hits = pygame.sprite.spritecollide(p, terrains, False)
        if hits :
            lowest = hits[0]
            for hit in hits:
                if hit.rect.bottom > lowest.rect.bottom:
                    lowest = hit
            if p.rect.bottom >= lowest.rect.top and p.rect.bottom <= lowest.rect.bottom :
                p.speedy = 0
                p.accely = 0
                p.rect.bottom = lowest.rect.top
            else : p.accely = 0.5
        else :
            p.accely = 0.5

    # check to see if the cannonballs hit terrains.
    hits = pygame.sprite.groupcollide(cannonballs, terrains, True, True)
    if hits:
        for hit in hits:
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
        




    
    # Draw / render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    
    pygame.display.flip()

pygame.quit()
