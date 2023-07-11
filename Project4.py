#background image : "https://www.freepik.com/free-vector/arcade-game-world-pixel-scene_4815143.htm#query=game%20background%20pixel%20terrain&position=1&from_view=search&track=ais">Image by stockgiu
#cannon image : "https://www.flaticon.com/free-icons/army" title="army icons">Army icons created by Freepik - Flaticon
#cannonball image : "https://www.flaticon.com/free-icons/bomb" title="bomb icons">Bomb icons created by Freepik - Flaticon

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

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_hp_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 12
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, startingPosition):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.image.set_colorkey(BLACK)
        
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
        old_center = self.rect.center
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
            cannonballs1.add(cannonball)
           
        
class Cannonball1(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self)

        self.image = cannonball_img
        self.image.set_colorkey(WHITE)
        

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = vy
        self.speedx = vx
        self.accely = 0.5

        self.time_generated = pygame.time.get_ticks()
        self.now = pygame.time.get_ticks()
        self.timedelay = 60

    def update(self):
        self.now = pygame.time.get_ticks()
        self.rect.x += self.speedx
        self.speedy += self.accely
        self.rect.y += self.speedy
        
        # kill if it moves off the top of the screen
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
        self.length = random.randrange(100, 199)
        self.image = terrain_img[self.length-100]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.length)
        self.rect.y = random.randrange(int(HEIGHT/3) , HEIGHT)
        




# Load all game graphics
background_orig = pygame.image.load(path.join(img_dir, "45908.jpg")).convert()
background = pygame.transform.scale(background_orig,(1800,1000))
cannon_img = pygame.image.load(path.join(img_dir, "cannon_img.png")).convert()
player_img = pygame.image.load(path.join(img_dir, "tank.png")).convert()
cannonball_img_orig = pygame.image.load(path.join(img_dir, "bomb.png")).convert()
cannonball_img = pygame.transform.scale(cannonball_img_orig, (30, 30))
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
terrain_img_orig = pygame.image.load(path.join(img_dir, "37692.jpg")).convert()
terrain_img = []
for i in range(100):
    terrain_img.append(pygame.transform.scale(terrain_img_orig, (i+100, 30)))

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
cannonballs1 = pygame.sprite.Group()
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
            elif event.key == pygame.K_PAGEUP:
                if Turn == 1:
                    player1.cannon_mag += 1
                elif Turn == 0:
                    player2.cannon_mag += 1
            elif event.key == pygame.K_PAGEDOWN:
                if Turn == 1:
                    player1.cannon_mag -= 1
                elif Turn == 0:
                    player2.cannon_mag -= 1
            
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
    hits = pygame.sprite.groupcollide(cannonballs1, terrains, True, True)
    if hits:
        for hit in hits:
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)

    # check to see if the cannonballs hit players
    hits = pygame.sprite.groupcollide(cannonballs1, players, False, False)
    if hits:
        for hit in hits:
            if hit.now - hit.time_generated > hit.timedelay:
                expl = Explosion(hit.rect.center, 'lg')
                all_sprites.add(expl)
                hits[hit][0].hp -= 10
                hit.kill()
        




    

    # Draw / render
    screen.fill(WHITE)
    screen.blit(background, background.get_rect())
    all_sprites.draw(screen)



    draw_hp_bar(screen, 85, 13, player1.hp)
    draw_hp_bar(screen, WIDTH-200, 13, player2.hp)

    draw_text(screen, "Player1", 20, 40, 7)
    draw_text(screen, "Player2", 20, WIDTH-50, 7)

    draw_text(screen, f"Magnitude : {player1.cannon_mag}", 20, 73, 30)
    draw_text(screen, f"Magnitude : {player2.cannon_mag}", 20, WIDTH-80, 30)

    for p in players :
        vector_angle = p.cannon_mag * np.array([np.cos(np.deg2rad(p.cannon_angle)), np.sin(np.deg2rad(p.cannon_angle))])
        pygame.draw.line(screen, BLACK, p.rect.center, p.rect.center+vector_angle, 5)
    

    
    pygame.display.flip()

pygame.quit()
