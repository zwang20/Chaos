import pygame
import os
from sge import *
import random
import sys
import math

# init pygame
pygame.init()

# create clock
clock = pygame.time.Clock()

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# creat window
display_width = 800
display_height = 800
display = pygame.display.set_mode([display_width, display_height])

# set caption
pygame.display.set_caption('Chaos')

# set icon
pygame.display.set_icon(
    pygame.image.load(os.path.join('assets', '32x32_project_nont.png'))
)

# Disable Mouse
pygame.mouse.set_visible(False)


# Load images
rifle_img = pygame.image.load(os.path.join('Assets', 'guns', 'gun_rifle.png'))
sniper_rifle_img = pygame.image.load(os.path.join('Assets', 'guns', 'gun_sniper.png'))


# load sounds
pistol_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'M1911.ogg'))
rifle_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'M16.ogg'))
reload_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'Reload.ogg'))


# sound channels
CHANNELS = 20
pygame.mixer.set_num_channels(CHANNELS)


class GameObj(pygame.sprite.Sprite):

    family = pygame.sprite.RenderUpdates()

    def __init__(self):
        super().__init__()
        GameObj.family.add(self)


class Block(GameObj):

    family = pygame.sprite.Group()

    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        Block.family.add(self)


class Enemy(GameObj):

    family = pygame.sprite.Group()

    width = 10
    height = 10

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        Enemy.family.add(self)

    def move(self, x, y):

        # left and right
        self.rect.x += x

        # Screen edge
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x + Enemy.width >= display_width:
            self.rect.x = display_width - Enemy.width

        # Did this update cause us to hit a wall?
        for i in pygame.sprite.spritecollide(self, Block.family, False):
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if x > 0:
                self.rect.right = i.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = i.rect.right

        # up and down
        self.rect.y += y

        # Screen edge
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y + Enemy.height >= display_width:
            self.rect.y = display_width - Enemy.height

        # Did this update cause us to hit a wall?
        for i in pygame.sprite.spritecollide(self, Block.family, False):
             # Reset our position based on the top/bottom of the object.
            if y > 0:
                self.rect.bottom = i.rect.top
            else:
                self.rect.top = i.rect.bottom

    def ai(self):
        if self.rect.x > Player.family.sprite.rect.x:
            self.move(-1, 0)
        else:
            self.move(1, 0)
        if self.rect.y > Player.family.sprite.rect.y:
            self.move(0, -1)
        else:
            self.move(0, 1)

    def update(self):
        self.ai()
        if pygame.sprite.spritecollide(self, Player.family, False):
            print('You died')


class Bullet(GameObj):

    family = pygame.sprite.Group()

    width = 2
    height = 10

    def __init__(self, x, y, angle, velocity):
        super().__init__()
        self._x = x
        self._y = y
        self.angle = angle
        self.velocity = velocity
        self.vector_x = velocity * math.sin(math.radians(self.angle))
        self.vector_y = velocity * -math.cos(math.radians(self.angle))
        self.image_ori = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image_ori.fill(BLACK)
        self.image = pygame.transform.rotate(self.image_ori, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        Bullet.family.add(self)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = value

    def update(self):
        if 0 <= self.rect.x <= display_width and 0 <= self.rect.y <= display_height:
            self.x += self.vector_x
            self.y += self.vector_y
        else:
            self.kill()

        if pygame.sprite.spritecollide(self, Enemy.family, True):
            smart_spawn()
            smart_spawn()

        if pygame.sprite.spritecollide(self, Block.family, False):
            self.kill()


class Player(GameObj):

    family = pygame.sprite.GroupSingle() # only one sprite

    width = 10
    height = 10
    angle = 0
    weapon = 0
    health = 100

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = 0
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        Player.family.add(self)

    def move(self, x, y):

        # left and right
        self.rect.x += x

        # Screen edge
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x + Player.width >= display_width:
            self.rect.x = display_width - Player.width

        # Did this update cause us to hit a wall?
        for i in pygame.sprite.spritecollide(self, Block.family, False):
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if x > 0:
                self.rect.right = i.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = i.rect.right

        # up and down
        self.rect.y += y

        # Screen edge
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y + Player.height >= display_width:
            self.rect.y = display_width - Player.height

        # Did this update cause us to hit a wall?
        for i in pygame.sprite.spritecollide(self, Block.family, False):
             # Reset our position based on the top/bottom of the object.
            if y > 0:
                self.rect.bottom = i.rect.top
            else:
                self.rect.top = i.rect.bottom

    def get_angle(self):
        get_angle_mouse_pos = pygame.mouse.get_pos()
        get_angle_mouse_x = get_angle_mouse_pos[0]
        get_angle_mouse_y = get_angle_mouse_pos[1]
        get_angle_player_x = self.rect.x + self.width/2
        get_angle_player_y = self.rect.y + self.height/2
        get_angle_difference_x = abs(get_angle_mouse_x - get_angle_player_x)
        get_angle_difference_y = abs(get_angle_mouse_y - get_angle_player_y)
        # seperate into 4 quadrents
        if get_angle_mouse_x > get_angle_player_x: # right of Player
            if get_angle_mouse_y < get_angle_player_y: # quadrent 1
                return math.degrees(math.atan(get_angle_difference_x/get_angle_difference_y))
            elif get_angle_mouse_y > get_angle_player_y: # quadrent 2
                return 90 + math.degrees(math.atan(get_angle_difference_y/get_angle_difference_x))
        elif get_angle_mouse_x < get_angle_player_x: # left of Player
            if get_angle_mouse_y < get_angle_player_y: # quadrent 4
                return 270 + math.degrees(math.atan(get_angle_difference_y/get_angle_difference_x))
            elif get_angle_mouse_y > get_angle_player_y: # quadrent 3
                return 180 + math.degrees(math.atan(get_angle_difference_x/get_angle_difference_y))
        elif get_angle_difference_x == 0: # same left&right
            if get_angle_difference_y == 0: # same point
                return 0
            elif get_angle_mouse_y < get_angle_player_y: # above
                return 0
            elif get_angle_mouse_y > get_angle_player_y: # below
                return 180
        if get_angle_difference_y == 0: # same elevation
            if get_angle_mouse_x < get_angle_player_x: # left
                return 270
            elif get_angle_mouse_x > get_angle_player_x: # right
                return 90
        return 0

def smart_spawn():
    Enemy(random.randint(1, display_width - Enemy.height - 1),
          random.randint(1, display_width - Enemy.width - 1))



def get_input():
    if pygame.event.peek(pygame.QUIT):
        pygame.quit()
        sys.exit()


def update():
    GameObj.family.update()


def game():

    # Debug
    DEBUG = False

    player = Player(400, 400)

    # cooldown
    cooldown = 0

    # weapons
    weapons = {
    0: {'name': 'M1911', 'max_ammo': 7,  'cooldown_time': 10, 'burst': False, 'burst_count': 1, 'burst_time': 0, 'reload_time': 60 , 'ammo' : 7 , 'sound': pistol_sound},
    1: {'name': 'M16'  , 'max_ammo': 20, 'cooldown_time': 8, 'burst': False, 'burst_count': 2, 'burst_time': 2, 'reload_time': 180, 'ammo' : 20, 'sound': rifle_sound }
    }

    Block(100, 100, 10, 600)
    Block(100, 100, 600, 10)
    Block(100, 120, 500, 10)

    # Main loop
    smart_spawn()

    # bullet spread
    spread = 1

    # ammo
    reload = 0
    max_ammo = weapons[player.weapon]['max_ammo']
    burst = weapons[player.weapon]['burst']
    channel = 0

    while True:
        # initilasion
        clock.tick(60)  # Frames per second
        sge_clear(display)  # Clear

        display_text = '  '.join([str(int(10*clock.get_fps())/10), str(weapons[player.weapon]['name']), ' '.join([str(weapons[player.weapon]['ammo']), '/', str(max_ammo)])])

        sge_print(display, display_text) # display text

        # fire
        fire = False

        # pause
        pause = False

        # Input
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        get_input()

        if keys[pygame.K_q] and (keys[pygame.K_LMETA] or keys[pygame.K_RMETA]):  # Quit
            pygame.quit()
            sys.exit()

        if keys[pygame.K_e] and (keys[pygame.K_LMETA] or keys[pygame.K_RMETA]):  # Quit
            DEBUG = not DEBUG

        if keys[pygame.K_w] or keys[pygame.K_UP]:  # Up
            player.move(0, -3)

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # Right
            player.move(3, 0)

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # Left
            player.move(-3, 0)

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # Down
            player.move(0, 3)

        # change weapon
        if keys[pygame.K_1]:
            player.weapon = 0

        if keys[pygame.K_2]:
            player.weapon = 1

        # Pause
        if keys[pygame.K_p]:
            pause = True

        # Pause
        while pause:
            clock.tick(10)
            sge_clear(display)
            sge_print(display, 'Paused')
            sge_print(display, 'To unpause press x', 1, 30)
            keys = pygame.key.get_pressed()
            get_input()
            if keys[pygame.K_x]:
                pause = False
            pygame.display.update()  # update
            # This should be the last thing in the loop

        # fire input
        if mouse[0] or keys[pygame.K_SPACE]:
            fire = True

        # mouse
        sge_rect(display, mouse_pos[0]-8, mouse_pos[1]-1, 16, 2, RED)
        sge_rect(display, mouse_pos[0]-1, mouse_pos[1]-8, 2, 16, RED)

        # temperory mouse
        temp_spread_x = random.uniform(-spread, spread)
        temp_spread_y = random.uniform(-spread, spread)

        # Debug
        if DEBUG:
            pygame.draw.line(game_display, BLACK, (player.rect.x+Player.width/2, player.rect.y +
                                                   player.height/2), (mouse_pos[0]+temp_spread_x, mouse_pos[1]+temp_spread_y), 2)
            cooldown = 0
            weapons[player.weapon]['ammo'] = 1


        player.angle = Player.get_angle(player)

        cooldown_time = weapons[player.weapon]['cooldown_time']
        max_ammo = weapons[player.weapon]['max_ammo']
        reload_time = weapons[player.weapon]['reload_time']
        burst_time = weapons[player.weapon]['burst_time']

        # Fire
        if fire and cooldown == 0 and weapons[player.weapon]['ammo']:

            # cooldown

            if weapons[player.weapon]['burst']:
                if burst == 0:
                    cooldown += cooldown_time
                    burst = weapons[player.weapon]['burst_count']
                else:
                    burst -= 1
            else:
                cooldown += cooldown_time


            # bullet here
            Bullet(player.rect.x + player.width/2, player.rect.y + player.height/2, player.angle + random.randint(-spread, spread), 20)


            # sound
            pygame.mixer.Channel(channel).play(weapons[player.weapon]['sound'])
            channel += 1

            # ammo
            weapons[player.weapon]['ammo'] -= 1
            # reload sound
            if channel > CHANNELS - 1:
                channel = 0
            if not weapons[player.weapon]['ammo']:
                pygame.mixer.Channel(channel).play(reload_sound)
                channel += 1

        # Cooldown
        if cooldown > 0:
            cooldown -= 1

        # reload
        if not weapons[player.weapon]['ammo']:
            reload += 1

        if reload >= reload_time:
            weapons[player.weapon]['ammo'] = max_ammo
            reload = 0

        update()

        # print(GameObj.family.sprites())

        GameObj.family.draw(display) # draw sprites

        if channel > CHANNELS - 1:
            channel = 0

        pygame.display.update()  # update
        # This should be the last thing in the loop


game()
