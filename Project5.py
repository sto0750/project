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
def draw_text(surf, text, size, x, y, color = BLACK):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
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

# def draw_exp_bar(surf, x, y, pct):
#     BAR_LENGTH = 100
#     BAR_HEIGHT = 10
#     if pct > BAR_LENGTH:
#         pct = pct % BAR_LENGTH
#     fill = (pct / 100) * BAR_LENGTH
#     outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
#     fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
#     pygame.draw.rect(surf, YELLOW, fill_rect)
#     pygame.draw.rect(surf, WHITE, outline_rect, 2)

# def draw_lives(surf, x, y, lives, img):
#     for i in range(lives):
#         img_rect = img.get_rect()
#         img_rect.x = x + 30 * i
#         img_rect.y = y
#         surf.blit(img, img_rect)

# def LevelUp():
#     player.power += 1
#     screen.blit(background, background_rect)
#     draw_text(screen, "LEVEL UP!", 64, WIDTH / 2, HEIGHT / 4)
#     draw_text(screen, f"LEVEL {player.level}", 22,
#               WIDTH / 2, HEIGHT / 2)
#     pygame.display.flip()
#     starttime = pygame.time.get_ticks()
#     time = 0
#     while time < 600:
#         time = pygame.time.get_ticks() - starttime
#         clock.tick(FPS)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()

#     newmob()


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

        self.shooting_chance = 3


    def update(self):
        self.rect.x += self.speedx
        self.speedy += self.accely
        self.rect.y += self.speedy
        self.cannon_angle  += self.cannon_anglespeed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


        
    def shoot(self):
        if self.shooting_chance > 0:
            vx = self.cannon_mag * np.cos(np.deg2rad(self.cannon_angle))
            vy = self.cannon_mag * np.sin(np.deg2rad(self.cannon_angle))
            if self.cannon_type == 1:
                cannonball = Cannonball1(self.rect.centerx, self.rect.centery, vx, vy)
                all_sprites.add(cannonball)
                cannonballs1.add(cannonball)
            self.shooting_chance -= 1
            #shoot_sound.play()
        # if self.power == 2:
        #     bullet1 = Bullet(self.rect.left, self.rect.centery)
        #     bullet2 = Bullet(self.rect.right, self.rect.centery)
        #     all_sprites.add(bullet1)
        #     all_sprites.add(bullet2)
        #     bullets.add(bullet1)
        #     bullets.add(bullet2)
        #     shoot_sound.play()
        # if self.power == 3:
        #     bullet = Bullet(self.rect.centerx, self.rect.top)
        #     bullet1 = Bullet(self.rect.left, self.rect.centery)
        #     bullet2 = Bullet(self.rect.right, self.rect.centery)
        #     all_sprites.add(bullet)
        #     all_sprites.add(bullet1)
        #     all_sprites.add(bullet2)
        #     bullets.add(bullet)
        #     bullets.add(bullet1)
        #     bullets.add(bullet2)
        #     shoot_sound.play()
        
        # if self.power >= 4:
        #     bullet1 = Bullet(self.rect.centerx, self.rect.top)
        #     bullet2 = Bullet(self.rect.left, self.rect.centery)
        #     bullet3 = Bullet(self.rect.right, self.rect.centery)
        #     bullet2.speedx = -1
        #     bullet3.speedx = 1
        #     all_sprites.add(bullet1)
        #     all_sprites.add(bullet2)
        #     all_sprites.add(bullet3)
        #     bullets.add(bullet1)
        #     bullets.add(bullet2)
        #     bullets.add(bullet3)
        #     shoot_sound.play()


    # def hide(self):
    #     # hide the player temporarily
    #     self.hidden = True
    #     self.hide_timer = pygame.time.get_ticks()
    #     self.rect.center = (WIDTH / 2, HEIGHT + 200)



    
        


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

# class Pow(pygame.sprite.Sprite):
#     def __init__(self, center):
#         pygame.sprite.Sprite.__init__(self)
#         self.type = random.choice(['shield', 'gun'])
#         self.image = powerup_images[self.type]
#         self.image.set_colorkey(BLACK)
#         self.rect = self.image.get_rect()
#         self.rect.center = center
#         self.speedy = 5

#     def update(self):
#         self.rect.y += self.speedy
#         # kill if it moves off the top of the screen
#         if self.rect.top > HEIGHT:
#             self.kill()

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
        


def show_go_screen():
    screen.blit(background, background.get_rect())
    draw_text(screen, "SHMUP!", 128, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Right/Left to move, Up/Down to adjust angle, PgUp/PgDw to adjust power, Space to fire",
              44, WIDTH / 2, HEIGHT / 2, (232, 83, 19))
    draw_text(screen, "Press a key to begin", 36, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_between_turns():
    screen.blit(background, background.get_rect())
    draw_text(screen, f"Player{2 - Turn}'s Turn", 128, WIDTH / 2, HEIGHT / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Load all game graphics
background_orig = pygame.image.load(path.join(img_dir, "45908.jpg")).convert()
background = pygame.transform.scale(background_orig,(1800,1000))
player_img = pygame.image.load(path.join(img_dir, "tank.png")).convert()
cannonball_img_orig = pygame.image.load(path.join(img_dir, "bomb.png")).convert()
cannonball_img = pygame.transform.scale(cannonball_img_orig, (30, 30))
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
terrain_img_orig = pygame.image.load(path.join(img_dir, "37692.jpg")).convert()
terrain_img = []
for i in range(100):
    terrain_img.append(pygame.transform.scale(terrain_img_orig, (i+100, 30)))
# background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
# background_rect = background.get_rect()
# player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
# player_mini_img = pygame.transform.scale(player_img, (25, 19))
# player_mini_img.set_colorkey(BLACK)
# bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
# meteor_images = []
# meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
#                'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
#                'meteorBrown_tiny1.png']
# for img in meteor_list:
#     meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())


# powerup_images = {}
# powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
# powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()


# # Load all game sounds
# shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'flaunch.wav'))
# shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav'))
# power_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))
# expl_sounds = []
# for snd in ['expl3.wav', 'expl6.wav']:
#     expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
# player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
# pygame.mixer.music.load(path.join(snd_dir, 'Spiky Candy - Comet.mp3'))
# pygame.mixer.music.set_volume(0.4)

# pygame.mixer.music.play(loops=-1)
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
        show_go_screen()
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
                show_between_turns()

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
        




    # check to see if a bullet hit a mob
    # for b in bullets:
    #     for m in pygame.sprite.spritecollide(b, mobs, False):
    #         print(m.hardness)
    #         m.hardness -= 1

    # hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
    # for hit in hits:
    #     if hit.hardness <= 0:
    #         hit.kill()
    #         score += 50 - hit.radius
    #         player.exp += hit.radius / 10
    #         if player.exp > 100:
    #             player.exp -= 100
    #             player.level += 1
    #             Hardness += 1
    #             LevelUp()
    #         random.choice(expl_sounds).play()
    #         expl = Explosion(hit.rect.center, 'lg')
    #         all_sprites.add(expl)
    #         if random.random() > 0.9:
    #             pow = Pow(hit.rect.center)
    #             all_sprites.add(pow)
    #             powerups.add(pow)
    #         newmob()

    # # check to see if a mob hit the player
    # hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    # for hit in hits:
    #     player.shield -= hit.radius * 2
    #     expl = Explosion(hit.rect.center, 'sm')
    #     all_sprites.add(expl)
    #     newmob()
    #     if player.shield <= 0:
    #         player_die_sound.play()
    #         death_explosion = Explosion(player.rect.center, 'player')
    #         all_sprites.add(death_explosion)
    #         player.hide()
    #         player.lives -= 1
    #         player.shield = 100

    # # check to see if player hit a powerup
    # hits = pygame.sprite.spritecollide(player, powerups, True)
    # for hit in hits:
    #     if hit.type == 'shield':
    #         player.shield += random.randrange(10, 30)
    #         shield_sound.play()
    #         if player.shield >= 100:
    #             player.shield = 100
    #     if hit.type == 'gun':
    #         player.powerup()
    #         power_sound.play()

    # # if the player died and the explosion has finished playing
    # if player.lives == 0 and not death_explosion.alive():
    #     game_over = True

    # if one player shoots every chances, then it switches turn automatically
    for p in players:
        if p.shooting_chance <= 0 and not cannonballs1:
            now = pygame.time.get_ticks()
            Turn = (Turn + 1) % 2
            if pygame.time.get_ticks() - now > 90:
                show_between_turns()
                p.shooting_chance = 3

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
    

    #draw_exp_bar(screen, 5, 17, player.exp)
    #draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
