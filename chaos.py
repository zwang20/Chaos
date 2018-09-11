import pygame
import os
from sge import *

# init pygame
pygame.init()

# create clock
clock = pygame.time.Clock()

# colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# creat windows
game_display = pygame.display.set_mode([800, 800])

# set caption
pygame.display.set_caption('Project nont')

# set icon
pygame.display.set_icon(
pygame.image.load(os.path.join('assets', '32x32_project_nont.png'))
)

# Disable Mouse
pygame.mouse.set_visible(False)

# create bullets list
bullets = [] # x, y, vector x, vextor y

# Init cooldown
cooldown = 0

# position
pos = [400, 400]

# Main loop
while True:

    # init
    clock.tick(30) # Frames per second
    sge_clear(game_display) # Clear
    sge_print(game_display, str(int(10*clock.get_fps())/10)) # Fps display

    # fire
    fire = False

    # pause
    pause = False

    # Input
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    for event in pygame.event.get():  # Input
        if event.type == pygame.QUIT: # Quit
            pygame.display.quit()
            pygame.quit()
            quit()

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
        clock.tick(30)
        sge_clear(game_display)
        sge_print(game_display, 'Paused')
        sge_print(game_display, 'To unpause press x', 1, 30)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():  # Input
            if event.type == pygame.QUIT: # Quit
                pygame.display.quit()
                pygame.quit()
                quit()
        if keys[pygame.K_q]:
            pygame.display.quit()
            pygame.quit()
            quit()
        if keys[pygame.K_x]:
            pause = False
        pygame.display.update() # update
        # This should be the last thing in the loop

    # fire input
    if mouse[0] or keys[pygame.K_SPACE]:
        fire = True

    # mouse
    sge_rect(game_display, mouse_pos[0]-8, mouse_pos[1]-1, 16, 2, red)
    sge_rect(game_display, mouse_pos[0]-1, mouse_pos[1]-8, 2, 16, red)

    # player
    sge_rect(game_display, *pos, 10, 10)
    # start temp
    # temp ratios
    temp = (((((mouse_pos[0]-pos[0])**2)+((mouse_pos[1]-pos[1])**2))**0.5)/10)

    # temp ZeroDivision error
    if temp == 0:
        temp = 0.1

    # Fire
    if fire and cooldown < 100 and cooldown%4 == 0:

        bullets.append(
        [*pos, (mouse_pos[0]-pos[0])/temp, (mouse_pos[1]-pos[1])/temp]
        )

        cooldown +=10

    # end temp
    del temp

    # Cooldown
    if cooldown > 0:
        cooldown -= 1

    # Cooldown bar
    sge_rect(game_display, 700, 790, 100, 10, white)
    sge_rect(game_display, 700, 790, cooldown, 10, red)

    # Bullets movement
    # start bullets_temp
    bullets_temp = []
    for bullet in bullets:

        # move
        bullets_temp.append(
        [bullet[0]+bullet[2], bullet[1]+bullet[3], bullet[2], bullet[3]]
        )

        # display bullets
        sge_line(
        game_display, black, (bullet[0], bullet[1]),
        (bullet[0]-bullet[2], bullet[1]-bullet[3]), 2
        )

    bullets = bullets_temp
    del bullets_temp

    # del extra bullets
    if len(bullets) > 100:
        del bullets[0]


    pygame.display.update() # update
    # This should be the last thing in the loop
