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

# position
pos = [400, 400]

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

    def __init__(self):
        self.x = 400
        self.y = 400
        Player.objects.append(self)

    def display():
        for i in Player.objects:
            pygame.draw.rect(display, blue, (i.x, i.y, Player.width, Player.height))

    def move(self, x, y):
        self.x += x
        self.y += y

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
            if e.x < i.x < (e.x + Enemy.width) and e.y < i.y < (e.y + Enemy.width):
                Enemy.objects.remove(e)
                Bullet.objects.remove(i)
                smart_spawn()
        for b in Block.objects:
            if b.x < i.x < (b.x + b.width) and b.y < i.y < (b.y + b.width):
                Bullet.objects.remove(i)


def smart_spawn():
    Enemy(random.randint(1, display_width - Enemy.height - 1), random.randint(1, display_width - Enemy.width - 1))

def get_input():
    if pygame.event.peek(pygame.QUIT) or pygame.key.get_pressed()[pygame.K_q]:
        pygame.quit()
        quit()

def game():

    # Init cooldown
    cooldown = 0
    Block(200, 200, 100, 100)
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
            if pos[1] > 0:
                pos[1] -= 3

        if keys[pygame.K_d]:  # Right
            if pos[0] < 790:
                pos[0] += 3

        if keys[pygame.K_a]:  # Left
            if pos[0] > 0:
                pos[0] -= 3

        if keys[pygame.K_s]:  # Down
            if pos[1] < 790:
                pos[1] += 3

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
        sge_rect(display, *pos, 10, 10)
        # start temp
        # temp ratios
        temp = (((((mouse_pos[0]-pos[0])**2)+((mouse_pos[1]-pos[1])**2))**0.5)/10)

        # temp ZeroDivision error
        if temp != 0:

            # Fire
            if fire and cooldown < 100 and cooldown%4 == 0:

                Bullet(*pos, (mouse_pos[0]-pos[0])/temp, (mouse_pos[1]-pos[1])/temp)
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
