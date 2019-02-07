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


class GameObj(pygame.sprite.Sprite):
    family = pygame.sprite.RenderUpdates()

    def __init__(self):
        super().__init__()
        GameObj.family.add(self)


class Block(GameObj):

    family = pygame.sprite.RenderUpdates()

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        super().__init__()
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.family.add(self)


class Enemy:
    objects = []
    width = 10
    height = 10

    def __init__(self, x, y):
        Enemy.objects.append(self)
        self.x = x
        self.y = y

    def display():
        for i in Enemy.objects:
            pygame.draw.rect(
                display, RED, (i.x, i.y, Enemy.width, Enemy.height))

    def move():
        for i in Enemy.objects:
            pass

    def ai():
        pass


class Bullet:
    objects = []

    def __init__(self, x, y, angle, velocity):
        self.x = x
        self.y = y
        self.angle = angle
        self.velocity = velocity
        Bullet.objects.append(self)
        self.vector_x = velocity * math.sin(math.radians(self.angle))
        self.vector_y = velocity * -math.cos(math.radians(self.angle))

    def display():
        for i in Bullet.objects:
            pygame.draw.line(
                display, BLACK, (i.x, i.y), (i.x+i.vector_x*10/i.velocity, i.y+i.vector_y*10/i.velocity), 2)

    def renew():
        for i in Bullet.objects:
            if 0 <= i.x <= display_width and 0 <= i.y <= display_height:
                i.x += i.vector_x
                i.y += i.vector_y
            else:
                try:
                    Bullet.objects.remove(i)
                except ValueError:
                    pass


class Player(GameObj):

    family = pygame.sprite.RenderUpdates()

    width = 10
    height = 10
    angle = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        super().__init__()
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.family.add(self)

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.x + Player.width >= display_width:
            self.rect.x = display_width - Player.width
        if self.rect.y + Player.height >= display_width:
            self.rect.y = display_width - Player.height

        # add collision_detection

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


def collision_detection():
    for i in Bullet.objects:
        for e in Enemy.objects:
            if (e.x < i.x < (e.x + Enemy.width) and e.y < i.y < (e.y + Enemy.height)) or (e.x < i.x + i.vector_x < (e.x + Enemy.width) and e.y < i.y + i.vector_y < (e.y + Enemy.height)):
                try:
                    Enemy.objects.remove(e)
                    Bullet.objects.remove(i)
                except ValueError:
                    pass
                if len(Enemy.objects) == 0 or int(clock.get_fps()) > 25:
                    smart_spawn()
                if int(clock.get_fps()) > 25:
                    smart_spawn()
    # add collision_detection


def smart_spawn():
    Enemy(random.randint(1, display_width - Enemy.height - 1),
          random.randint(1, display_width - Enemy.width - 1))
    # add block collision_detection


def get_input():
    if pygame.event.peek(pygame.QUIT):
        pygame.quit()
        sys.exit()


def renew():
    pass

def game():

    # Debug
    DEBUG = False

    player = Player(400, 400)

    # Init cooldown
    cooldown = 0

    # Block(300, 300, 200, 200)

    # Main loop
    smart_spawn()

    # bullet spread
    spread = 1

    while True:
        # initilasion
        clock.tick(60)  # Frames per second
        sge_clear(display)  # Clear
        sge_print(display, str(int(10*clock.get_fps())/10))  # Fps display

        # Enemy.display()
        collision_detection()
        Bullet.renew()
        Bullet.display()

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


        player.angle = Player.get_angle(player)


        # Fire
        if fire and cooldown < 100 and cooldown % 4 == 0:

            # bullet here
            Bullet(player.rect.x + player.width/2, player.rect.y + player.height/2, player.angle + random.randint(-spread, spread), 20)

            #cooldown
            cooldown += 10


        # Cooldown
        if cooldown > 0:
            cooldown -= 1

        # Cooldown bar
        sge_rect(display, 700, 790, 100, 10, WHITE)
        sge_rect(display, 700, 790, cooldown, 10, RED)

        renew()

        GameObj.family.draw(display) # draw sprites

        pygame.display.update()  # update
        # This should be the last thing in the loop


game()
