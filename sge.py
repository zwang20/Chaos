import pygame
from data import *

if __name__ != "__main__":
    print('Simple Game Engine by Michael imported!')


def sge_print(
        display=game_display, string='Test', x=0, y=0, colour=(0, 0, 0)):
    display.blit(
        pygame.font.SysFont(
            "arial", 25).render(str(string), True, colour), (x, y))


def sge_rect(
        display=game_display, x=0, y=0, width=10, height=10, colour=(0, 0, 0)):
    if x <= 0:
        x = 1
    if y <= 0:
        y = 1
    if width <= 0:
        width = 1
    if height <= 0:
        height = 1
    return pygame.draw.rect(display, colour, (x, y, width, height))


def sge_clear(display=game_display, colour=(255, 255, 255)):
    display.fill(colour)


def sge_line(
    display=game_display,
    colour=(0, 0, 0), point_1=(0, 0), point_2=(10, 10), width=(10)):
    pygame.draw.line(display, colour, point_1, point_2, width)


def sge_load():
    try:
        x = open('settings.dat', 'r')
        y = x.read()
        x.close()
        z = y.split('\n')
        e = []
        for t in z:
            if t:
                e.append(t.split(' = '))
        return dict(e)
    except FileNotFoundError:
        x = open('settings.dat', 'w')
        x.close()
        return None


def sge_write(var, value):
    var = str(var)
    value = str(value)
    try:
        x = open('settings.dat', 'r')
        x.close
    except FileNotFoundError:
        x = open('settings.dat', 'w')
        x.close()
    x = open('settings.dat', 'r')
    y = x.read()
    x.close()
    z = y.split('\n')
    e = []
    for t in z:
        if t:
            e.append(t.split(' = '))
    g = dict(e)
    try:
        g[var]
    except KeyError:
        x = open('settings.dat', 'a')
        x.write(''.join([var, ' = ', value]))
    else:
        x = open('settings.dat', 'r')
        y = x.read()
        x.close()
        x = open('settings.dat', 'w')
        x.write(y)
        x.close()
