import pygame
import sys
# * means everything
# pygame.locals has global variables
from pygame.locals import *


W = 1600
H = 900
horizontalSprites = 1
verticalSprites = 2
WHITE = (255, 255, 255)
SPEED = 5
WITCH_WIDTH = 100
GAME = True


class Background:
    def __init__(self, init_x, init_y, image):
        self.x = init_x
        self.y = init_y
        self.image = pygame.image.load(image)
        self.size = self.image.get_rect().size

    def scroll_right(self):
        if self.x + self.size[0] > SPEED:
            self.x -= SPEED

    def scroll_left(self):
        if self.x < SPEED:
            self.x += SPEED


class Character:
    def __init__(self, x, y, image, bg):
        self.x = x
        self.y = y
        self.background = bg
        # Loading function
        self.image = pygame.image.load(image)
        self.size = self.image.get_rect().size
        self.positionX = 0
        self.positionY = 0

    def get_size(self):
        return self.size

    def move_left(self):
        if self.x >= SPEED:
            self.x -= SPEED
            self.positionX = 0
            self.positionY = 0
            self.background.scroll_left()

    def move_right(self):
        if self.x <= (W - WITCH_WIDTH):
            self.x += SPEED
            self.positionX = 0
            self.positionY = self.size[0]
            self.background.scroll_right()


DISPLAYSURF = pygame.display.set_mode((W, H))

pygame.init()
pygame.display.set_caption("Yay!")

background = Background(0, 0, "test_background.png")
purl = Character(100, 100, "Sulba_spriteSheet.png", background)

while True:
    while GAME:
        DISPLAYSURF.fill(WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            purl.move_left()
        if keys[K_RIGHT]:
            purl.move_right()
        if keys[K_p]:
            GAME = False
        characterSize = purl.get_size()

        DISPLAYSURF.blit(background.image, (background.x, background.y))
        DISPLAYSURF.blit(purl.image, (purl.x, purl.y),
                            (purl.positionX, purl.positionY, characterSize[0]/horizontalSprites,
                            characterSize[1]/verticalSprites))
        pygame.display.update()
    keys = pygame.key.get_pressed()
    if keys[K_p]:
        GAME = True

    characterSize = purl.get_size()

    DISPLAYSURF.blit(background.image, (background.x, background.y))
    DISPLAYSURF.blit(purl.image, (purl.x, purl.y),
                        (purl.positionX, purl.positionY, characterSize[0]/horizontalSprites,
                        characterSize[1]/verticalSprites))
    pygame.display.update()
