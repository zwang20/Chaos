import pygame
import sys

pygame.init()

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

class GameObj(pygame.sprite.Sprite):
    family = pygame.sprite.RenderUpdates()

    def __init__(self):
        super().__init__()
        GameObj.family.add(self)


class Block(GameObj):

    # collision_detection
    family = pygame.sprite.Group()

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        Block.family.add(self)


def game():
    Block(GREEN, 100, 100)
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and (keys[pygame.K_LMETA] or keys[pygame.K_RMETA]) or pygame.event.peek(pygame.QUIT):  # Quit
            pygame.quit()
            sys.exit()
        GameObj.family.draw(display)
        pygame.display.update()
game()
