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
        self.rect = self.image.get_rect()
       
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
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -2
        if keystate[pygame.K_RIGHT]:
            self.speedx = 2
            # should control the magnitude of the cannonball shooting ( not done yet )

        self.rect.x += self.speedx
        self.speedy += self.accely
        self.rect.y += self.speedy
        self.cannon_angle  += self.cannon_anglespeed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
        print(self.rect.x, self.cannon_angle)



    def shoot(self):
        vx = self.cannon_mag * np.cos(np.deg2rad(self.cannon_angle))
        vy = self.cannon_mag * np.sin(np.deg2rad(self.cannon_angle))
        if self.cannon_type == 1:
            cannonball = Cannonball1(self.rect.centerx, self.rect.centery, vx, vy)
            all_sprites.add(cannonball)
            cannonballs.add(cannonball)


# class Cannon(pygame.sprite.Sprite):
#     def __init__(self, player):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.transform.scale(cannon_img, (40, 40))
#         self.image.set_colorkey(BLACK)

#         self.image_orig = pygame.transform.scale(cannon_img, (150, 300))
#         self.image_orig.set_colorkey(BLACK)
#         self.image = self.image_orig.copy()
#         self.rect = self.image.get_rect()
#         self.player = player
        
#         self.rect.bottom = player.rect.centery
#         self.rect.centerx = player.rect.centerx
#         self.rot = 0
#         self.rot_speed = 0

#     def rotate(self):
#         keystate = pygame.key.get_pressed()
#         if keystate[pygame.K_UP]:
#             self.rot_speed = -2
#         if keystate[pygame.K_DOWN]:
#             self.rot_speed = 2
#         self.rot = (self.rot + self.rot_speed) % 360
#         new_image = pygame.transform.rotate(self.image_orig, self.rot)
#         self.image = new_image

#     def update(self):
#         #self.rotate()
#         self.rect.x = self.player.rect.x
#         self.rect.y = self.player.rect.y
    
        


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

class Terrrain(pygame.sprite.Sprite):
    def __init__(self,):
        pygame.sprite.Sprite.__init__(self)
        self.length = random.randrange(100, 200)
        self.image = pygame.Surface((self.length, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.length)
        self.rect.y = random.randrange(int(HEIGHT/3) , HEIGHT)
        

# Load all game graphics
cannon_img = pygame.image.load(path.join(img_dir, "cannon_img.png")).convert()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()

# Game loop
game_over = True
running = True

all_sprites = pygame.sprite.Group()
cannonballs = pygame.sprite.Group()
terrains = pygame.sprite.Group()
for i in range(180):
    t = Terrrain()
    all_sprites.add(t)
    terrains.add(t)
player1 = Player((WIDTH/2. , 70))

all_sprites.add(player1)

while running:
    if game_over:
        game_over = False
        

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
                player1.shoot()
            elif event.key == pygame.K_UP:
                player1.cannon_anglespeed -= 1.
            elif event.key == pygame.K_DOWN:
                player1.cannon_anglespeed += 1.
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player1.cannon_anglespeed = 0

    # Update
    all_sprites.update()

    # check to see if the player lands on a terrain.
    hits = pygame.sprite.spritecollide(player1, terrains, False)
    if hits :
        lowest = hits[0]
        for hit in hits:
            if hit.rect.bottom > lowest.rect.bottom:
                lowest = hit
        if player1.rect.bottom >= lowest.rect.top and player1.rect.bottom <= lowest.rect.bottom :
            player1.speedy = 0
            player1.accely = 0
            player1.rect.bottom = lowest.rect.top
        else : player1.accely = 0.5
    else :
        player1.accely = 0.5

    # Draw / render
    screen.fill(WHITE)
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
