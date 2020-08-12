# import system packages
import os
import random
import sys
import math
import time

# import third party package
import pygame

# init pygame
pygame.init()

# create clock
clock = pygame.time.Clock()

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255); GREY = (128, 128, 128)
RED = (255, 0, 0); DARK_READ = (128, 0, 0)
GREEN = (0, 255, 0); DARK_GREEN = (0, 128, 0)
BLUE = (0, 0, 255); DARK_BLUE = (0, 0, 128)
CYAN = (0, 255, 255); DARK_CYAN = (0, 128, 128)
MAGENTA = (255, 0, 255); DARK_MAGENTA = (128, 0, 128)
YELLOW = (255, 255, 0); DARK_YELLOW = (128, 128, 0)

# creat window
display_width = 1280
display_height = 800
display = pygame.display.set_mode([display_width, display_height],)

# TODO: fix this
game_display = display

# set caption
pygame.display.set_caption('Chaos')

# set icon
pygame.display.set_icon(pygame.image.load(os.path.join('assets', '32x32_project_nont.png')))

# Load images
rifle_img = pygame.image.load(os.path.join('Assets', 'guns', 'gun_rifle.png'))
sniper_rifle_img = pygame.image.load(os.path.join('Assets', 'guns', 'gun_sniper.png'))

# load sounds
pistol_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'M1911.ogg'))
rifle_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'M16.ogg'))
reload_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'Reload.ogg'))

# sound channels
CHANNELS = 100
pygame.mixer.set_num_channels(CHANNELS)


class GameObj(pygame.sprite.Sprite):

    family = pygame.sprite.RenderUpdates()

    def __init__(self):
        super().__init__()
        GameObj.family.add(self)


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
        if self.rect.y + Enemy.height >= display_height:
            self.rect.y = display_height - Enemy.height

        # Did this update cause us to hit a wall?
        for i in pygame.sprite.spritecollide(self, Block.family, False):
             # Reset our position based on the top/bottom of the object.
            if y > 0:
                self.rect.bottom = i.rect.top
            else:
                self.rect.top = i.rect.bottom

    def ai(self):
        if pygame.sprite.spritecollide(self, PathBlockEnemy.family, False):
            for x in PathBlockEnemy.objects:
                if pygame.sprite.collide_rect(self, x):
                    for y in PathBlockPlayer.family:
                        if x.id == y.id:
                            if pygame.sprite.spritecollide(y, Player.family, False):
                                self.move(x.move_x, x.move_y)
                                return

        if self.rect.x > Player.family.sprite.rect.x:
            self.move(-1, 0)
        elif self.rect.x == Player.family.sprite.rect.x:
            pass
        else:
            self.move(1, 0)
        if self.rect.y > Player.family.sprite.rect.y:
            self.move(0, -1)
        elif self.rect.y == Player.family.sprite.rect.y:
            pass
        else:
            self.move(0, 1)

    def update(self):
        self.ai()
        if pygame.sprite.spritecollide(self, Player.family, False):
            Player.family.sprite.score -= 1


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
            Player.family.sprite.score += 1
            self.kill()

        if pygame.sprite.spritecollide(self, Block.family, False):
            self.kill()


class Player(GameObj):

    family = pygame.sprite.GroupSingle() # only one sprite

    width = 10
    height = 10
    angle = 0
    weapon = 1
    health = 100
    score = 0
    weapons = {}
    _ammo = {
        1:  100,
        2:  100,
    }
    _clip_ammo = {
        1:  7,
    }

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
        if self.rect.y + Player.height >= display_height:
            self.rect.y = display_height - Player.height

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

    def get_ammo(self, id):
        try:
            return self._ammo[id]
        except KeyError:
            return 0

    def change_ammo(self, id, amount):
        try:
            self._ammo[id] += amount
        except KeyError:
            if amount < 0:
                print(('Error: Gun Id {} ammo was set to {}').format(id, amount))
            else:
                self._ammo[id] = amount

    def get_clip_ammo(self, id):
        try:
            return self._clip_ammo[id]
        except KeyError:
            return 0

    def change_clip_ammo(self, id, amount):
        try:
            self._clip_ammo[id] += amount
        except KeyError:
            self._clip_ammo[id] = amount

class PathBlockEnemy(pygame.sprite.Sprite):
    objects = []

    family = pygame.sprite.Group()

    def __init__(self, x, y, width, height, move_x, move_y, id):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.move_x = move_x
        self.move_y = move_y
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        PathBlockEnemy.family.add(self)
        self.id = id
        PathBlockEnemy.objects.append(self)


class PathBlockPlayer(pygame.sprite.Sprite):

    family = pygame.sprite.Group()

    def __init__(self, x, y, width, height, id):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        PathBlockPlayer.family.add(self)
        self.id = id


def smart_spawn():
    Enemy(random.randint(1, display_width - Enemy.width - 1),
          random.randint(1, display_height - Enemy.height - 1))


def get_input():
    if pygame.event.peek(pygame.QUIT):
        pygame.quit()
        sys.exit()


def update():
    GameObj.family.update()


def main_menu():
    while True:
        clock.tick(60)
        display.fill(WHITE)
        text = pygame.font.SysFont("arial", 100).render(str('Chaos'), True, BLACK)
        display.blit(text, (display_width/2 - text.get_width()/2, display_height/5 - text.get_height()/2))

        # play button
        play_button = pygame.Rect(0, 0, display_width/2, display_height/10)
        play_button.center = (display_width/2, display_height/2)
        pygame.draw.rect(game_display, GREEN, play_button)
        if play_button.left <= pygame.mouse.get_pos()[0] <= play_button.right and play_button.top <= pygame.mouse.get_pos()[1] <= play_button.bottom:
            pygame.draw.rect(game_display, DARK_GREEN, play_button)
            if pygame.mouse.get_pressed()[0]:
                game()
        text = pygame.font.SysFont("arial", 30).render(str('Start Game'), True, BLACK)
        display.blit(text, (play_button.centerx - text.get_width() / 2, play_button.centery - text.get_height() / 2))

        get_input()
        if pygame.event.peek(pygame.QUIT) or (pygame.key.get_pressed()[pygame.K_q] and (pygame.key.get_pressed()[pygame.K_LMETA] or pygame.key.get_pressed()[pygame.K_RMETA])):
            pygame.quit()
            sys.exit()
        pygame.display.update()  # update
        # This should be the last thing in the loop


def game():

    # Disable Mouse
    # pygame.mouse.set_visible(False)

    # Debug
    DEBUG = False

    player = Player(display_width/2, display_height/2)

    # cooldown
    cooldown = 0

    # weapons_old
    # weapons_old = {
    # 0: {'name': 'M1911',  'max_ammo': 7,  'cooldown_time': 10, 'burst': False, 'burst_count': 1, 'burst_time': 0, 'reload_time': 60 , 'ammo' : 7 , 'sound': pistol_sound},
    # 1: {'name': 'M16'  ,  'max_ammo': 20, 'cooldown_time': 8,  'burst': True,  'burst_count': 3, 'burst_time': 2, 'reload_time': 180, 'ammo' : 20, 'sound': rifle_sound },
    # 2: {'name': 'Test 1', 'max_ammo': 50, 'cooldown_time': 5,  'burst': False, 'burst_count': 1, 'burst_time': 0, 'reload_time': 180, 'ammo' : 50, 'sound': rifle_sound },
    # 3: {'name': 'Test 2', 'max_ammo': 99, 'cooldown_time': 1,  'burst': False, 'burst_count': 1, 'burst_time': 0, 'reload_time': 0,   'ammo' : 50, 'sound': rifle_sound },
    # }

    weapons = {
        1: {
            'id':               1,
            'name':             'M1911',
            'clip_ammo':        7,
            'automatic':        False,
            'cooldown_time':    10,
            'burst':            0,
            'burst_time':       0,
            'reload_time':      60,
            'sound':            pistol_sound,
        },
        2: {
            'id':               2,
            'name':             'M16A4',
            'clip_ammo':        20,
            'automatic':        False,
            'cooldown_time':    10,
            'burst':            2,
            'burst_time':       2,
            'reload_time':      180,
            'sound':            rifle_sound,
        },
    }

    player.weapons[1] = weapons[1]
    player.weapons[2] = weapons[2]
    # player_weapons = weapons

    # deprecated
    # file = open(os.path.join('Assets', 'maps', 'map.map'), 'r')

    # safety
    # SAFE_WORDS = ['Block']
    # UNSAFE_WORDS = ['quit', 'exit', 'open', '#', '"', "'"]
    # for line in file.readlines():
    #     for word in SAFE_WORDS:
    #         if word not in line:
    #             raise KeyboardInterrupt
    #     for word in UNSAFE_WORDS:
    #         if word in line:
    #             raise KeyboardInterrupt
    # exec(file.read())

    # for line in file:
    #     eval(line) # This is extremely dangerous due to the ability to run code

    # Main loop
    # smart_spawn()

    # bullet spread
    spread = 1

    # ammo
    reload = 0
    clip_ammo = player.weapons[1]['clip_ammo']
    burst = player.weapons[1]['burst']
    automatic = player.weapons[1]['automatic']
    # ammo = player.get_ammo(player.weapon)
    # max_ammo = weapons_old[player.weapon]['max_ammo']
    # burst = weapons_old[player.weapon]['burst']
    channel = 0
    reloading = False
    bursting = False
    bursted = False
    burst_count = 0
    burst_cooldown = 0


    while True:
        # initilasion
        clock.tick(60)  # Frames per second
        # sge_clear(display)  # Clear
        display.fill(WHITE)

        display_text = '  '.join([

            # FPS
            'FPS:', str(int(10*clock.get_fps())/10),

            # Weapon
            str(player.weapons[player.weapon]['name']),
            # str(weapons_old[player.weapon]['name']),

            # Ammo
            # str(player.weapons[player.weapon]["clip_ammo"]),
            str(player.get_clip_ammo(player.weapon)),
            '/',
            str(player.get_ammo(player.weapon)),
            # str(weapons_old[player.weapon]['ammo']), '/', str(max_ammo),

            # Score
            'Score:', str(player.score)
        ])


        # sge_print(display, display_text) # display text

        display.blit(
            pygame.font.SysFont("arial", 15).render(
                str(display_text),
                True,
                BLACK,
            ),
            (0, 0),
        )

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
            player.weapon = 1

        if keys[pygame.K_2]:
            player.weapon = 2

        # if keys[pygame.K_3]:
        #     player.weapon = 3
        #
        # if keys[pygame.K_4]:
        #     player.weapon = 4

        # Pause
        if keys[pygame.K_p] or keys[pygame.K_ESCAPE]:
            pause = True

        # Pause
        while pause:
            clock.tick(10)
            # sge_clear(display)
            display.fill(WHITE)

            display.blit(
                pygame.font.SysFont("arial", 15).render(
                    str('Paused'),
                    True,
                    BLACK,
                ), (0, 0)
            )

            display.blit(
                pygame.font.SysFont("arial", 15).render(
                    str('To unpause press x'),
                    True,
                    BLACK,
                ), (1, 30)
            )

            # sge_print(display, 'Paused')
            # sge_print(display, 'To unpause press x', 1, 30)
            keys = pygame.key.get_pressed()
            get_input()
            if keys[pygame.K_x]:
                pause = False
            pygame.display.update()  # update
            # This should be the last thing in the loop

        # fire input
        if mouse[0] or keys[pygame.K_SPACE]:
            fire = True

        if not (mouse[0] or keys[pygame.K_SPACE]):
            bursted = False

        # mouse
        # sge_rect(display, mouse_pos[0]-8, mouse_pos[1]-1, 16, 2, RED)
        # sge_rect(display, mouse_pos[0]-1, mouse_pos[1]-8, 2, 16, RED)

        # temperory mouse
        temp_spread_x = random.uniform(-spread, spread)
        temp_spread_y = random.uniform(-spread, spread)

        # Debug
        # if DEBUG:
        #     pygame.draw.line(game_display, BLACK, (player.rect.x+Player.width/2, player.rect.y +
        #                                            player.height/2), (mouse_pos[0]+temp_spread_x, mouse_pos[1]+temp_spread_y), 2)
        #     cooldown = 0
        #     weapons_old[player.weapon]['ammo'] = 1


        player.angle = Player.get_angle(player)

        # cooldown_time = weapons_old[player.weapon]['cooldown_time']
        # max_ammo = weapons_old[player.weapon]['max_ammo']
        # reload_time = weapons_old[player.weapon]['reload_time']
        # burst_time = weapons_old[player.weapon]['burst_time']

        #
        # gun things
        clip_ammo = player.get_clip_ammo(player.weapon)
        burst = player.weapons[player.weapon]['burst']
        automatic = player.weapons[player.weapon]['automatic']

        # Fire
        # print(burst_cooldown)
        if fire:
            if not bursted:
                if player.get_clip_ammo(player.weapon):
                    if (not cooldown) or (not burst_cooldown):

                        if not cooldown:
                            # increase cooldown
                            cooldown += player.weapons[player.weapon]['cooldown_time']

                        if burst:
                            # print(1)
                            if not burst_cooldown:
                                # print(2)
                                burst_cooldown += player.weapons[player.weapon]['burst_time']



                        # sound
                        pygame.mixer.Channel(channel).play(player.weapons[player.weapon]['sound'])
                        channel += 1

                        # bullet here
                        Bullet(player.rect.x + player.width/2, player.rect.y + player.height/2, player.angle + random.randint(-spread, spread), 20)


                        # decrease ammo
                        player.change_clip_ammo(player.weapon, -1)

                        # semi automatic
                        if not player.weapons[player.weapon]['automatic']:
                            if burst_count >= burst:
                                bursted = True
                                burst_count = 0
                                bursting = False
                            else:
                                burst_count += 1
                                bursting = True
                            # print(1)

        # cooldown
        if cooldown > 0:
            cooldown -= 1
        if burst_cooldown > 0:
            burst_cooldown -= 1

        # TODO: fix this
        if player.get_clip_ammo(player.weapon) == 0:
            if player.get_ammo(player.weapon) > 0:
                reloading = True

        # reload
        if reloading == True:
            reload += 1

        if reload >= player.weapons[player.weapon]['reload_time']:
            reloading = False
            player.change_clip_ammo(player.weapon, player.weapons[player.weapon]["clip_ammo"])
            player.change_ammo(player.weapon, -player.weapons[player.weapon]["clip_ammo"])
            reload = 0
            pygame.mixer.Channel(channel).play(reload_sound)
            channel += 1

        update()

        # print(GameObj.family.sprites())

        GameObj.family.draw(display) # draw sprites

        if channel > CHANNELS - 1:
            channel = 0

        pygame.display.update()  # update
        # This should be the last thing in the loop


main_menu()
