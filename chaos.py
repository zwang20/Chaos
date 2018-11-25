import pygame
import os
from sge import *
import random

# init pygame
pygame.init()

# create clock
clock = pygame.time.Clock()

# colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# creat windows
display_width = 800
display_height = 800
display = pygame.display.set_mode([display_width, display_height])

# set caption
pygame.display.set_caption('Project nont')

# set icon
pygame.display.set_icon(pygame.image.load(os.path.join('assets', '32x32_project_nont.png')))

# Disable Mouse
pygame.mouse.set_visible(False)

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
            pygame.draw.rect(display, red, (i.x, i.y, Enemy.width, Enemy.height))


class Bullet:
    objects = []

    def __init__(self, x, y, vector_x, vector_y):
        self.x = x
        self.y = y
        self.vector_x = vector_x
        self.vector_y = vector_y
        Bullet.objects.append(self)

    def display():
        for i in Bullet.objects:
            pygame.draw.line(display, black, (i.x, i.y), (i.x+i.vector_x, i.y+i.vector_y), 2)

    def renew():
        for i in Bullet.objects:
            if 0 < i.x < display_width and 0 < i.y < display_height:
                i.x += i.vector_x
                i.y += i.vector_y


class Player:
    objects = []
    width = 10
    height = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        Player.objects.append(self)

    def display(self):
        for i in Player.objects:
            pygame.draw.rect(display, blue, (i.x, i.y, Player.width, Player.height))

    def move(self, x, y):
        self.x += x
        self.y += y
        if self.x <= 0:
            self.x = 0
        if self.y <= 0:
            self.y = 0
        if self.x + Player.width >= display_width:
            self.x = display_width - Player.width
        if self.y + Player.height >= display_width:
            self.y = display_width - Player.height
        for b in Block.objects:
            if (b.x < self.x < b.x + b.width or b.x < self.x + Player.width < b.x + b.width) and (b.y < self.y < b.y + b.length or b.y < self.y + Player.height < b.y + b.length):
                if x > 0:
                    self.x = b.x - Player.width
                if x < 0:
                    self.x = b.x + b.width
                if y > 0:
                    self.y = b.y - Player.height
                if y < 0:
                    self.y = b.y + b.length

class Block:
    objects = []

    def __init__(self, x, y, width, length):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        Block.objects.append(self)

    def display():
        for i in Block.objects:
            pygame.draw.rect(display, black, (i.x, i.y, i.width, i.length))


def collision_detection():
    for i in Bullet.objects:
        for e in Enemy.objects:
            if e.x < i.x < (e.x + Enemy.width) and e.y < i.y < (e.y + Enemy.height):
                Enemy.objects.remove(e)
                Bullet.objects.remove(i)
                smart_spawn()
    for i in Bullet.objects:
        for b in Block.objects:
            if b.x < i.x < (b.x + b.width) and b.y < i.y < (b.y + b.length):
                Bullet.objects.remove(i)


def smart_spawn():
    Enemy(random.randint(1, display_width - Enemy.height - 1), random.randint(1, display_width - Enemy.width - 1))
    for e in Enemy.objects:
        for b in Block.objects:
            if (b.x < e.x < b.x + b.width or b.x < e.x + e.width < b.x + b.width) and (b.y < e.y < b.y + b.length or b.y < e.y + e.height < b.y + b.length):
                Enemy.objects.remove(e)
                smart_spawn()


def get_input():
    if pygame.event.peek(pygame.QUIT) or pygame.key.get_pressed()[pygame.K_q]:
        pygame.quit()
        quit()


def game():

    player = Player(400, 400)

    # Init cooldown
    cooldown = 0
    Block(100, 100, 600, 100)
    Block(100, 600, 600, 100)
    # Main loop
    smart_spawn()
    while True:

        # init
        clock.tick(30) # Frames per second
        sge_clear(display) # Clear
        sge_print(display, str(int(10*clock.get_fps())/10)) # Fps display

        Enemy.display()
        collision_detection()
        Bullet.renew()
        Bullet.display()
        Block.display()
        player.display()

        # fire
        fire = False

        # pause
        pause = False

        # Input
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        get_input()

        if keys[pygame.K_q]:  # Quit
            pygame.display.quit()
            pygame.quit()
            quit()

        if keys[pygame.K_w]:  # Up
            player.move(0, -3)

        if keys[pygame.K_d]:  # Right
            player.move(3, 0)

        if keys[pygame.K_a]:  # Left
            player.move(-3, 0)

        if keys[pygame.K_s]:  # Down
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
            pygame.display.update() # update
            # This should be the last thing in the loop

        # fire input
        if mouse[0] or keys[pygame.K_SPACE]:
            fire = True

        # mouse
        sge_rect(display, mouse_pos[0]-8, mouse_pos[1]-1, 16, 2, red)
        sge_rect(display, mouse_pos[0]-1, mouse_pos[1]-8, 2, 16, red)

        # player
        # sge_rect(display, player.x, player.y, 10, 10)
        # start temp
        # temp ratios
        temp = (((((mouse_pos[0]-player.x)**2)+((mouse_pos[1]-player.y)**2))**0.5)/10)

        # temp ZeroDivision error
        if temp != 0:

            # Fire
            if fire and cooldown < 100 and cooldown%4 == 0:

                Bullet(player.x, player.y, (mouse_pos[0]-player.x)/temp, (mouse_pos[1]-player.y)/temp)
                cooldown +=10

        # end temp
        del temp

        # Cooldown
        if cooldown > 0:
            cooldown -= 1

        # Cooldown bar
        sge_rect(display, 700, 790, 100, 10, white)
        sge_rect(display, 700, 790, cooldown, 10, red)

        pygame.display.update() # update
        # This should be the last thing in the loop

game()
